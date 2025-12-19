#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE - 2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test utilities for agent modules.

This module is a grab-bag of helpers used by the test suite and other
development scripts:

- Structured types for test data and results (enums + dataclasses).
- A mock AI backend for deterministic testing.
- Fixture/test-data generators and filesystem isolation helpers.
- Snapshot testing utilities.
- Convenience helpers for logging capture and environment detection.

Legacy / compatibility helpers
------------------------------
Some functions at the end of the file are intentionally preserved to support
older tests that load modules by path (including hyphenated filenames) and/or
temporarily adjust `sys.path`.

This module is not intended to be executed as a CLI.
"""

from __future__ import annotations
import hashlib
import importlib.util
import json
import logging
import os
import re
import shutil
import sys
import tempfile
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Dict, Iterator, List, Optional, Set, Tuple, TypeVar, Union

import random

T = TypeVar("T")

try:
    import numpy as np
except ImportError:
    np = None  # type: ignore


# ============================================================================
# Type - Safe Enums for Test Utilities
# ============================================================================
class TestStatus(Enum):
    """Status of a test execution."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    PENDING = "pending"


class MockResponseType(Enum):
    """Types of mock AI backend responses."""

    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"
    EMPTY = "empty"


class IsolationLevel(Enum):
    """File system isolation levels."""

    NONE = "none"
    TEMP_DIR = "temp_dir"
    COPY_ON_WRITE = "copy_on_write"
    SANDBOX = "sandbox"


class TestDataType(Enum):
    """Types of test data."""

    PYTHON_CODE = "python_code"
    MARKDOWN = "markdown"
    JSON = "json"
    YAML = "yaml"
    TEXT = "text"


class PerformanceMetricType(Enum):
    """Types of performance metrics."""

    EXECUTION_TIME = "execution_time"
    MEMORY_USAGE = "memory_usage"
    FILE_IO = "file_io"
    CPU_TIME = "cpu_time"


class CleanupStrategy(Enum):
    """Cleanup strategies for test resources."""

    IMMEDIATE = "immediate"
    DEFERRED = "deferred"
    ON_SUCCESS = "on_success"
    NEVER = "never"


# ============================================================================
# Dataclasses for Structured Test Data
# ============================================================================
@dataclass
class TestFixture:
    """A test fixture with setup and teardown.

    Attributes:
        name: Fixture name.
        setup_fn: Setup function.
        teardown_fn: Teardown function.
        scope: Fixture scope (function, class, module, session).
        data: Fixture data.
    """

    name: str
    setup_fn: Optional[Callable[[], Any]] = None
    teardown_fn: Optional[Callable[[Any], None]] = None
    scope: str = "function"
    data: Any = None


@dataclass
class MockResponse:
    """Mock AI backend response.

    Attributes:
        content: Response content.
        response_type: Type of response.
        latency_ms: Simulated latency.
        tokens_used: Simulated token count.
        error_message: Error message if applicable.
    """

    content: str = ""
    response_type: MockResponseType = MockResponseType.SUCCESS
    latency_ms: int = 100
    tokens_used: int = 0
    error_message: Optional[str] = None


@dataclass
class TestDataFactory:
    """Factory for generating test data.

    Attributes:
        data_type: Type of data to generate.
        template: Template for generation.
        variations: Number of variations to create.
        seed: Random seed for reproducibility.
    """

    data_type: TestDataType
    template: str = ""
    variations: int = 1
    seed: Optional[int] = None


@dataclass
class TestResult:
    """Result of a test execution.

    Attributes:
        test_name: Name of the test.
        status: Test status.
        duration_ms: Test duration.
        error_message: Error message if failed.
        assertions_count: Number of assertions.
        timestamp: When test was run.
    """

    test_name: str
    status: TestStatus
    duration_ms: float = 0.0
    error_message: Optional[str] = None
    assertions_count: int = 0
    timestamp: float = field(default_factory=time.time)


@dataclass
class PerformanceMetric:
    """Performance metric from test execution.

    Attributes:
        metric_type: Type of metric.
        value: Metric value.
        unit: Unit of measurement.
        test_name: Associated test.
        timestamp: When captured.
    """

    metric_type: PerformanceMetricType
    value: float
    unit: str
    test_name: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class TestEnvironment:
    """Test environment configuration.

    Attributes:
        name: Environment name.
        env_vars: Environment variables.
        temp_dir: Temporary directory.
        isolation_level: File system isolation.
        cleanup: Cleanup strategy.
    """

    name: str
    env_vars: Dict[str, str] = field(default_factory=lambda: {})
    temp_dir: Optional[Path] = None
    isolation_level: IsolationLevel = IsolationLevel.TEMP_DIR
    cleanup: CleanupStrategy = CleanupStrategy.IMMEDIATE


@dataclass
class TestSnapshot:
    """Snapshot for snapshot testing.

    Attributes:
        name: Snapshot name.
        content: Snapshot content.
        content_hash: Hash of content.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    name: str
    content: str
    content_hash: str = ""
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        """Compute content hash if not provided."""
        # Convert content to string if it's a dict or other type
        if isinstance(self.content, dict):
            content_str = json.dumps(self.content)
        else:
            content_str = str(self.content)
        if not self.content_hash:
            self.content_hash = hashlib.sha256(
                content_str.encode("utf-8")
            ).hexdigest()

    def __eq__(self, other: object) -> bool:
        # Compatibility: some tests compare a loaded snapshot directly
        # to a raw content object (e.g. dict).
        if isinstance(other, (dict, list, str, int, float, bool)):
            return self.content == other
        if isinstance(other, TestSnapshot):
            return (
                self.name == other.name
                and self.content == other.content
                and self.content_hash == other.content_hash
            )
        return False


@dataclass
class SnapshotComparisonResult:
    """Result of comparing snapshots.

    Attributes:
        matches: Whether snapshots match.
        expected: Expected content.
        actual: Actual content.
        snapshot_name: Name of the snapshot.
    """

    matches: bool
    expected: Any
    actual: Any
    snapshot_name: str

    @property
    def diff(self) -> Optional[str]:
        """Get a simple diff representation."""
        if self.matches:
            return None

        if isinstance(self.expected, dict) and isinstance(self.actual, dict):
            expected_str = json.dumps(self.expected, indent=2, default=str)  # type: ignore[arg-type]
            actual_str = json.dumps(self.actual, indent=2, default=str)  # type: ignore[arg-type]
        else:
            expected_str = str(self.expected)  # type: ignore[arg-type]
            actual_str = str(self.actual)  # type: ignore[arg-type]

        return f"Expected:\n{expected_str}\n\nActual:\n{actual_str}"


@dataclass
class TestAssertion:
    """Custom assertion for agent testing.

    Attributes:
        name: Assertion name.
        expected: Expected value.
        actual: Actual value.
        passed: Whether assertion passed.
        message: Assertion message.
    """

    name: str
    expected: Any
    actual: Any
    passed: bool = False
    message: str = ""


AGENT_DIR = Path(__file__).resolve().parent


# ============================================================================
# Mock AI Backend
# ============================================================================
class MockAIBackend:
    """Mock AI backend for testing.

    Provides configurable mock responses for AI backend calls
    without making real API requests.

    Example:
        mock=MockAIBackend()
        mock.add_response("prompt1", MockResponse(content="response"))
        result=mock.call("prompt1")
    """

    def __init__(self) -> None:
        """Initialize mock backend."""
        self._responses: Dict[str, MockResponse] = {}
        self._default_response = MockResponse(content="Mock response")
        self._call_history: List[Tuple[str, float]] = []
        self._response_sequence: List[MockResponse] = []
        self._sequence_index: int = 0

    def add_response(
        self,
        prompt_pattern: str,
        response: MockResponse,
    ) -> None:
        """Add mock response for a prompt pattern.

        Args:
            prompt_pattern: Prompt pattern (can be exact or regex).
            response: Mock response to return.
        """
        self._responses[prompt_pattern] = response
        logging.debug(f"Added mock response for pattern: {prompt_pattern}")

    def set_default_response(self, response: MockResponse) -> None:
        """Set default response for unmatched prompts.

        Args:
            response: Default mock response.
        """
        self._default_response = response

    def call(self, prompt: str) -> str:
        """Call mock backend with prompt.

        Args:
            prompt: Prompt to send.

        Returns:
            str: Mock response content.

        Raises:
            TimeoutError: If response type is TIMEOUT.
            RuntimeError: If response type is ERROR.
        """
        self._call_history.append((prompt, time.time()))

        # Use response sequence if available
        if self._response_sequence and self._sequence_index < len(self._response_sequence):
            response = self._response_sequence[self._sequence_index]
            self._sequence_index += 1
        else:
            # Find matching response
            response = self._default_response
            for pattern, resp in self._responses.items():
                if pattern in prompt or re.search(pattern, prompt):
                    response = resp
                    break

        # Simulate latency
        if response.latency_ms > 0:
            time.sleep(response.latency_ms / 1000)

        # Handle response types
        if response.response_type == MockResponseType.TIMEOUT:
            raise TimeoutError("Mock timeout")
        if response.response_type == MockResponseType.ERROR:
            raise RuntimeError(response.error_message or "Mock error")
        if response.response_type == MockResponseType.RATE_LIMITED:
            raise RuntimeError("Rate limited")
        if response.response_type == MockResponseType.EMPTY:
            return ""

        return response.content

    def add_response_sequence(self, responses: List[MockResponse]) -> None:
        """Add a sequence of responses for sequential calls.

        Args:
            responses: List of mock responses.
        """
        self._response_sequence = responses
        self._sequence_index = 0

    def set_error_response(self, response_type: MockResponseType, message: str) -> None:
        """Set an error response to be returned.

        Args:
            response_type: Type of error response.
            message: Error message.
        """
        self._default_response = MockResponse(
            response_type=response_type,
            error_message=message
        )

    def get_call_history(self) -> List[Tuple[str, float]]:
        """Get history of calls made."""
        return list(self._call_history)

    def clear(self) -> None:
        """Clear all mock responses and history."""
        self._responses.clear()
        self._call_history.clear()


# ============================================================================
# Test Fixture Generator
# ============================================================================
class FixtureFactory:
    """Factory for creating test fixtures.

    Creates pre-configured fixtures for tests including agents,
    files, and other resources with optional dependencies.
    """

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        """Initialize fixture factory.

        Args:
            base_dir: Base directory for file fixtures.
        """
        self.base_dir = base_dir or Path.cwd()

    def create_agent_fixture(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        dependencies: Optional[List[Any]] = None,
    ) -> Any:
        """Create an agent fixture.

        Args:
            name: Fixture name.
            config: Agent configuration.
            dependencies: List of dependent fixtures.

        Returns:
            Agent fixture object with name, config and dependencies attributes.
        """
        class AgentFixture:
            def __init__(self, name: str, config: Optional[Dict[str, Any]], dependencies: Optional[List[Any]]):
                self.name = name
                self.config = config or {}
                self.dependencies = dependencies or []

        return AgentFixture(name, config, dependencies)

    def create_file_fixture(self, name: str, content: str = "") -> Any:
        """Create a file fixture.

        Args:
            name: File name.
            content: File content.

        Returns:
            File fixture object with setup_fn method.
        """
        class FileFixture:
            def __init__(self, base_dir: Path, name: str, content: str):
                self.base_dir = base_dir
                self.name = name
                self.content = content

            def setup_fn(self) -> Path:
                """Set up the file and return its path."""
                path = self.base_dir / self.name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(self.content)
                return path

        return FileFixture(self.base_dir, name, content)


class TestDataSeeder:
    """Generates reproducible test data with optional seeding."""

    def __init__(self, seed: Optional[int] = None) -> None:
        """Initialize test data seeder.

        Args:
            seed: Random seed for reproducibility.
        """
        self.seed = seed
        # Use an instance RNG to avoid global-random interference across tests.
        self._rng = random.Random(seed)
        if seed is not None and np:
            np.random.seed(seed)

    def generate_metric_data(self, count: int = 10) -> List[Dict[str, Union[str, float]]]:
        """Generate metric data for testing.

        Args:
            count: Number of metrics to generate.

        Returns:
            List of metric dictionaries.
        """
        return [
            {
                "metric": f"metric_{i}",
                "value": self._rng.uniform(0, 100),
                "timestamp": time.time() + i
            }
            for i in range(count)
        ]

    def generate_test_results(self, count: int = 10, pass_rate: float = 0.8) -> List[Dict[str, Any]]:
        """Generate test results for testing.

        Args:
            count: Number of test results to generate.
            pass_rate: Fraction of tests that should pass.

        Returns:
            List of test result dictionaries.
        """
        return [
            {
                "test_name": f"test_{i}",
                "status": "PASSED" if self._rng.random() < pass_rate else "FAILED",
                "duration_ms": self._rng.uniform(10, 5000)
            }
            for i in range(count)
        ]

    def generate_file_content(self, language: str = "python") -> str:
        """Generate sample file content.

        Args:
            language: Programming language ("python", "javascript", etc.).

        Returns:
            Generated file content.
        """
        # Use a deterministic return value based on seed for reproducibility
        func_id = self.seed if self.seed is not None else self._rng.randint(1, 100)
        return_val = self._rng.randint(1, 100)
        if language == "python":
            return f'# Python file\ndef func_{func_id}():\n    return {return_val}\n'
        elif language == "javascript":
            return f'// JavaScript file\nfunction func_{func_id}() {{\n  return {return_val};\n}}\n'
        else:
            return f"// Generic content\nval_{func_id} = {return_val}\n"

    def generate_unique_id(self) -> str:
        """Generate a unique ID.

        Returns:
            Unique ID string.
        """
        return f"id_{int(time.time() * 1000000)}_{random.randint(1000, 9999)}"

    def generate_bulk_data(self, count: int = 10, data_type: str = "python_code") -> List[str]:
        """Generate bulk data.

        Args:
            count: Number of items to generate.
            data_type: Type of data to generate.

        Returns:
            List of generated data items.
        """
        if data_type == "python_code":
            return [f"def func_{i}():\n    return {i}\n" for i in range(count)]
        elif data_type == "ids":
            return [self.generate_unique_id() for _ in range(count)]
        else:
            return [f"item_{i}_{self.generate_unique_id()}" for i in range(count)]


class TestOutputFormatter:
    """Formats test output and results for display."""

    def __init__(self) -> None:
        """Initialize formatter."""
        self.results: List[Tuple[str, str, float]] = []

    @staticmethod
    def format_success(test_name: str, duration_ms: float) -> str:
        """Format a successful test result.

        Args:
            test_name: Name of the test.
            duration_ms: Duration of the test in milliseconds.

        Returns:
            Formatted success message.
        """
        return f"✓ {test_name} - PASSED ({duration_ms:.2f}ms)"

    @staticmethod
    def format_failure(test_name: str, error: str) -> str:
        """Format a failed test result.

        Args:
            test_name: Name of the test.
            error: Error message.

        Returns:
            Formatted failure message.
        """
        return f"✗ {test_name}: {error}"

    @staticmethod
    def format_summary(passed: int, failed: int, total: int) -> str:
        """Format test summary.

        Args:
            passed: Number of passed tests.
            failed: Number of failed tests.
            total: Total number of tests.

        Returns:
            Formatted summary.
        """
        return f"{passed} passed, {failed} failed out of {total} tests"

    def format_result(self, test_name: str, status: Any, duration_ms: float, error_message: str = "") -> str:
        """Format a test result based on status.

        Args:
            test_name: Name of the test.
            status: Status (TestStatus enum, str).
            duration_ms: Duration in milliseconds.
            error_message: Optional error message.

        Returns:
            Formatted result string.
        """
        # Handle TestStatus enum
        status_str = status.value if hasattr(status, 'value') else str(status)
        status_str = status_str.lower()

        if "pass" in status_str:
            return self.format_success(test_name, duration_ms)
        else:
            msg = f"{status_str}: {error_message}" if error_message else status_str
            return self.format_failure(test_name, msg)

    def add_result(self, test_name: str, status: Any, duration_ms: float) -> None:
        """Add a test result.

        Args:
            test_name: Name of the test.
            status: Status of the test.
            duration_ms: Duration in milliseconds.
        """
        status_str = status.value if hasattr(status, 'value') else str(status)
        self.results.append((test_name, status_str, duration_ms))

    def get_summary(self) -> Dict[str, int]:
        """Get a summary of all results as a dict.

        Returns:
            Summary dict with counts.
        """
        passed = sum(1 for _, status, _ in self.results if "pass" in status.lower())
        failed = sum(1 for _, status, _ in self.results if "fail" in status.lower())
        total = len(self.results)
        return {
            "passed": passed,
            "failed": failed,
            "total": total
        }


class AssertionHelpers:
    """Helper functions for common assertions in tests."""

    @staticmethod
    def assert_file_contains(file_path: Path, text: str) -> bool:
        """Assert that a file contains specific text.

        Args:
            file_path: Path to the file.
            text: Text to search for.

        Returns:
            True if assertion passes.

        Raises:
            AssertionError: If text is not found.
        """
        content = file_path.read_text()
        assert text in content, f"File {file_path} does not contain '{text}'"
        return True

    @staticmethod
    def assert_output_matches_pattern(output: str, pattern: str) -> bool:
        """Assert that output matches a regex pattern.

        Args:
            output: The output string.
            pattern: The regex pattern.

        Returns:
            True if assertion passes.

        Raises:
            AssertionError: If pattern does not match.
        """
        assert re.search(pattern, output), f"Output does not match pattern '{pattern}'"
        return True

    @staticmethod
    def assert_raises_with_message(
        fn: Callable[..., Any],
        exception_type: type[BaseException],
        message: str,
        *args: Any,
    ) -> bool:
        """Assert that a function raises an exception with a specific message.

        Args:
            fn: Function to call.
            exception_type: Expected exception type.
            message: Expected message text.
            *args: Arguments to pass to the function.

        Returns:
            True if assertion passes.

        Raises:
            AssertionError: If exception is not raised or message doesn't match.
        """
        try:
            fn(*args)
            raise AssertionError(f"Expected {exception_type.__name__} but no exception was raised")
        except BaseException as e:
            if isinstance(e, exception_type):
                assert message in str(e), f"Exception message '{str(e)}' does not contain '{message}'"
                return True
            raise


class TestTimer:
    """Timer for measuring test execution time."""

    def __init__(self) -> None:
        """Initialize timer."""
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def start(self) -> None:
        """Start the timer."""
        self.start_time = time.time()

    def stop(self) -> float:
        """Stop the timer and return elapsed time in seconds.

        Returns:
            Elapsed time in seconds.
        """
        self.end_time = time.time()
        if self.start_time is None:
            return 0.0
        return self.end_time - self.start_time

    @property
    def elapsed_ms(self) -> float:
        """Get elapsed time in milliseconds."""
        if self.start_time is None or self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time) * 1000


class Benchmarker:
    """Runs benchmarks and collects statistics."""

    def __init__(self) -> None:
        """Initialize benchmarker."""
        self.timings: List[float] = []

    def run(self, fn: Callable[[], None], iterations: int = 5) -> Dict[str, float]:
        """Run a function multiple times and collect timing statistics.

        Args:
            fn: Function to benchmark.
            iterations: Number of iterations.

        Returns:
            Statistics dictionary with min/max/mean in both seconds and milliseconds, plus iterations.
        """
        self.timings = []
        for _ in range(iterations):
            timer = TestTimer()
            timer.start()
            fn()
            elapsed = timer.stop()
            self.timings.append(elapsed)

        mean_seconds = sum(self.timings) / len(self.timings)
        return {
            "min": min(self.timings),
            "max": max(self.timings),
            "mean": mean_seconds,
            "median": sorted(self.timings)[len(self.timings) // 2],
            "min_ms": min(self.timings) * 1000,
            "max_ms": max(self.timings) * 1000,
            "average_ms": mean_seconds * 1000,
            "iterations": iterations
        }


class FixtureGenerator:
    """Generates test fixtures for common agent scenarios.

    Example:
        gen=FixtureGenerator()
        fixture=gen.create_python_file_fixture("test.py", "print('hello')")
    """

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        """Initialize fixture generator.

        Args:
            base_dir: Base directory for fixtures.
        """
        self.base_dir = base_dir or Path(tempfile.mkdtemp())
        self._fixtures: Dict[str, TestFixture] = {}

    def create_python_file_fixture(
        self,
        filename: str,
        content: str,
    ) -> TestFixture:
        """Create a Python file fixture.

        Args:
            filename: File name.
            content: File content.

        Returns:
            TestFixture: Created fixture.
        """
        file_path = self.base_dir / filename

        def setup() -> Path:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            return file_path

        def teardown(path: Path) -> None:
            if path.exists():
                path.unlink()

        fixture = TestFixture(
            name=filename,
            setup_fn=setup,
            teardown_fn=teardown,
        )
        self._fixtures[filename] = fixture
        return fixture

    def create_directory_fixture(
        self,
        dirname: str,
        files: Dict[str, str],
    ) -> TestFixture:
        """Create a directory fixture with files.

        Args:
            dirname: Directory name.
            files: Dict of filename to content.

        Returns:
            TestFixture: Created fixture.
        """
        dir_path = self.base_dir / dirname

        def setup() -> Path:
            dir_path.mkdir(parents=True, exist_ok=True)
            for name, content in files.items():
                (dir_path / name).write_text(content, encoding="utf-8")
            return dir_path

        def teardown(path: Path) -> None:
            if path.exists():
                shutil.rmtree(path)

        fixture = TestFixture(
            name=dirname,
            setup_fn=setup,
            teardown_fn=teardown,
        )
        self._fixtures[dirname] = fixture
        return fixture

    def cleanup_all(self) -> None:
        """Clean up all created fixtures."""
        for fixture in self._fixtures.values():
            if fixture.teardown_fn and fixture.data:
                try:
                    fixture.teardown_fn(fixture.data)
                except Exception as e:
                    logging.warning(f"Failed to cleanup fixture {fixture.name}: {e}")
        self._fixtures.clear()


# ============================================================================
# Test Data Factory
# ============================================================================
class TestDataGenerator:
    """Generates realistic test data for agent testing.

    Example:
        gen=TestDataGenerator()
        code=gen.generate_python_code(with_errors=False)
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        """Initialize data generator.

        Args:
            seed: Random seed for reproducibility.
        """
        self.seed = seed
        if seed:
            import random
            random.seed(seed)

    def generate_python_code(
        self,
        with_errors: bool = False,
        with_docstrings: bool = True,
        num_functions: int = 3,
    ) -> str:
        """Generate sample Python code.

        Args:
            with_errors: Include syntax errors.
            with_docstrings: Include docstrings.
            num_functions: Number of functions to generate.

        Returns:
            str: Generated Python code.
        """
        lines = ['"""Generated test module."""', "", "import os", ""]

        for i in range(num_functions):
            lines.append(f"def function_{i}(arg1, arg2):")
            if with_docstrings:
                lines.append(f'    """Function {i} docstring."""')
            if with_errors and i == 0:
                lines.append("    return arg1 +")  # Syntax error
            else:
                lines.append(f"    return arg1 + arg2 + {i}")
            lines.append("")

        return "\n".join(lines)

    def generate_markdown(
        self,
        with_headers: bool = True,
        with_code_blocks: bool = True,
        num_sections: int = 3,
    ) -> str:
        """Generate sample markdown content.

        Args:
            with_headers: Include headers.
            with_code_blocks: Include code blocks.
            num_sections: Number of sections.

        Returns:
            str: Generated markdown.
        """
        lines: List[str] = []
        if with_headers:
            lines.append("# Test Document")
            lines.append("")
        for i in range(num_sections):
            if with_headers:
                lines.append(f"## Section {i}")
            lines.append("")
            lines.append(f"This is section {i} content.")
            lines.append("")
            if with_code_blocks:
                lines.append("```python")
                lines.append(f"print('Section {i}')")
                lines.append("```")
                lines.append("")
        return "\n".join(lines)

    def generate_json(
        self,
        num_items: int = 5,
        nested: bool = True,
    ) -> str:
        """Generate sample JSON content.

        Args:
            num_items: Number of items.
            nested: Include nested structures.

        Returns:
            str: Generated JSON.
        """
        data: Dict[str, Any] = {
            "items": [
                {
                    "id": i,
                    "name": f"item_{i}",
                    "value": i * 10,
                }
                for i in range(num_items)
            ],
        }

        if nested:
            data["metadata"] = {
                "generated": datetime.now().isoformat(),
                "count": num_items,
            }

        return json.dumps(data, indent=2)


# ============================================================================
# File System Isolation
# ============================================================================
class FileSystemIsolator:
    """Isolates file system operations for testing.

    Example:
        with FileSystemIsolator() as fs:
            fs.write_file("test.txt", "content")
            content=fs.read_file("test.txt")
    """

    def __init__(
        self,
        isolation_level: IsolationLevel = IsolationLevel.TEMP_DIR,
    ) -> None:
        """Initialize file system isolator.

        Args:
            isolation_level: Level of isolation.
        """
        self.isolation_level = isolation_level
        self._temp_dir: Optional[Path] = None
        self._original_cwd: Optional[str] = None
        self._created_files: List[Path] = []

    def __enter__(self) -> "FileSystemIsolator":
        """Enter context and set up isolation."""
        if self.isolation_level == IsolationLevel.TEMP_DIR:
            self._temp_dir = Path(tempfile.mkdtemp())
            self._original_cwd = os.getcwd()
            os.chdir(self._temp_dir)
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit context and clean up."""
        if self._original_cwd:
            os.chdir(self._original_cwd)
        if self._temp_dir and self._temp_dir.exists():
            shutil.rmtree(self._temp_dir)
        self._created_files.clear()

    def write_file(self, path: str, content: str) -> Path:
        """Write a file in isolated environment.

        Args:
            path: File path.
            content: File content.

        Returns:
            Path: Path to created file.
        """
        file_path = Path(path)
        if self._temp_dir:
            file_path = self._temp_dir / path

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        self._created_files.append(file_path)
        return file_path

    def read_file(self, path: str) -> str:
        """Read a file from isolated environment.

        Args:
            path: File path.

        Returns:
            str: File content.
        """
        file_path = Path(path)
        if self._temp_dir:
            file_path = self._temp_dir / path
        return file_path.read_text(encoding="utf-8")

    def get_temp_dir(self) -> Optional[Path]:
        """Get the temporary directory."""
        return self._temp_dir


# ============================================================================
# Performance Tracker
# ============================================================================
class PerformanceTracker:
    """Tracks test execution performance.

    Example:
        tracker=PerformanceTracker()
        with tracker.track("test_function"):
            run_test()
        metrics=tracker.get_metrics()
    """

    def __init__(self) -> None:
        """Initialize performance tracker."""
        self._metrics: List[PerformanceMetric] = []
        self._start_times: Dict[str, float] = {}

    @contextmanager
    def track(self, test_name: str) -> Iterator[None]:
        """Track execution time for a test.

        Args:
            test_name: Name of the test.
        """
        start = time.time()
        self._start_times[test_name] = start
        try:
            yield
        finally:
            duration = (time.time() - start) * 1000  # ms
            metric = PerformanceMetric(
                metric_type=PerformanceMetricType.EXECUTION_TIME,
                value=duration,
                unit="ms",
                test_name=test_name,
            )
            self._metrics.append(metric)
            del self._start_times[test_name]

    def record_metric(
        self,
        test_name: str,
        metric_type: PerformanceMetricType,
        value: float,
        unit: str,
    ) -> None:
        """Record a performance metric.

        Args:
            test_name: Test name.
            metric_type: Type of metric.
            value: Metric value.
            unit: Unit of measurement.
        """
        metric = PerformanceMetric(
            metric_type=metric_type,
            value=value,
            unit=unit,
            test_name=test_name,
        )
        self._metrics.append(metric)

    def get_metrics(self) -> List[PerformanceMetric]:
        """Get all recorded metrics."""
        return list(self._metrics)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of performance metrics."""
        if not self._metrics:
            return {}

        execution_times = [
            m.value for m in self._metrics
            if m.metric_type == PerformanceMetricType.EXECUTION_TIME
        ]

        return {
            "total_metrics": len(self._metrics),
            "avg_execution_time_ms": (
                sum(execution_times) / len(execution_times)
                if execution_times else 0
            ),
            "max_execution_time_ms": max(execution_times) if execution_times else 0,
            "min_execution_time_ms": min(execution_times) if execution_times else 0,
        }

    def clear(self) -> None:
        """Clear all recorded metrics."""
        self._metrics.clear()
        self._start_times.clear()


# ============================================================================
# Snapshot Testing
# ============================================================================
class SnapshotManager:
    """Manages snapshots for snapshot testing.

    Example:
        mgr=SnapshotManager(Path("snapshots"))
        mgr.assert_match("test1", actual_output)
    """

    def __init__(self, snapshot_dir: Path) -> None:
        """Initialize snapshot manager.

        Args:
            snapshot_dir: Directory to store snapshots.
        """
        self.snapshot_dir = snapshot_dir
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self._snapshots: Dict[str, TestSnapshot] = {}

    def _get_snapshot_path(self, name: str) -> Path:
        """Get path for a snapshot."""
        return self.snapshot_dir / f"{name}.snap"

    def save_snapshot(self, name: str, content: Any) -> TestSnapshot:
        """Save a new snapshot.

        Args:
            name: Snapshot name.
            content: Snapshot content (str or dict/list).

        Returns:
            TestSnapshot: Created snapshot.
        """
        # Convert content to string for TestSnapshot
        if isinstance(content, str):
            content_str = content
            snapshot_content = content
        else:
            content_str = json.dumps(content, indent=2)
            snapshot_content = content_str

        path = self._get_snapshot_path(name)
        path.write_text(content_str, encoding="utf-8")
        snapshot = TestSnapshot(name=name, content=snapshot_content)
        self._snapshots[name] = snapshot
        return snapshot

    def load_snapshot(self, name: str) -> Optional[TestSnapshot]:
        """Load an existing snapshot.

        Args:
            name: Snapshot name.

        Returns:
            The loaded TestSnapshot object or None.
        """
        path = self._get_snapshot_path(name)
        if not path.exists():
            return None

        content_str = path.read_text(encoding="utf-8")
        # Try to parse as JSON
        try:
            content = json.loads(content_str)
        except json.JSONDecodeError:
            content = content_str

        # Return TestSnapshot object with the loaded content
        snapshot = TestSnapshot(name=name, content=content)
        self._snapshots[name] = snapshot
        return snapshot

    def compare_snapshot(self, name: str, actual: Any) -> "SnapshotComparisonResult":
        """Compare actual content with a saved snapshot.

        Args:
            name: Snapshot name.
            actual: Actual content to compare.

        Returns:
            SnapshotComparisonResult with comparison details.
        """
        expected_snapshot = self.load_snapshot(name)

        if expected_snapshot is None:
            return SnapshotComparisonResult(
                matches=False,
                expected=None,
                actual=actual,
                snapshot_name=name
            )

        # Compare the content
        matches = expected_snapshot.content == actual
        return SnapshotComparisonResult(
            matches=matches,
            expected=expected_snapshot.content,
            actual=actual,
            snapshot_name=name
        )

    def assert_match(
        self,
        name: str,
        actual: str,
        update: bool = False,
    ) -> bool:
        """Assert that actual matches snapshot.

        Args:
            name: Snapshot name.
            actual: Actual content.
            update: Update snapshot if mismatch.

        Returns:
            bool: True if match, False otherwise.
        """
        expected = self.load_snapshot(name)

        if expected is None:
            # No snapshot exists, create it
            self.save_snapshot(name, actual)
            return True

        if expected.content == actual:
            return True

        if update:
            self.save_snapshot(name, actual)
            return True

        return False

    def get_diff(self, name: str, actual: str) -> List[str]:
        """Get diff between snapshot and actual.

        Args:
            name: Snapshot name.
            actual: Actual content.

        Returns:
            List[str]: Diff lines.
        """
        import difflib
        expected = self.load_snapshot(name)
        if expected is None:
            return ["No snapshot exists"]
        return list(difflib.unified_diff(
            expected.content.splitlines(),
            actual.splitlines(),
            fromfile=f"snapshot/{name}",
            tofile="actual",
            lineterm="",
        ))


# ============================================================================
# Test Result Aggregator
# ============================================================================
class TestResultAggregator:
    """Aggregates test results for reporting.

    Example:
        agg=TestResultAggregator()
        agg.add_result(TestResult(name="test1", status=TestStatus.PASSED))
        report=agg.get_report()
    """

    def __init__(self) -> None:
        """Initialize result aggregator."""
        self._results: List[TestResult] = []

    def add_result(
        self,
        result: Union[TestResult, str],
        test_name: Optional[str] = None,
        status: Optional[str] = None,
    ) -> None:
        """Add a test result.

        Args:
            result: Test result object OR suite name (for backwards compatibility).
            test_name: Test name (when result is a string).
            status: Test status (when result is a string).
        """
        if isinstance(result, TestResult):
            self._results.append(result)
        elif test_name and status:
            # Support add_result(suite, test_name, status) style
            test_result = TestResult(
                test_name=f"{result}/{test_name}",
                status=TestStatus[status.upper()] if hasattr(TestStatus, status.upper()) else TestStatus.PASSED,
                duration_ms=0.0
            )
            self._results.append(test_result)
        else:
            raise TypeError("Invalid arguments to add_result")

    def get_results(self) -> List[TestResult]:
        """Get all results."""
        return list(self._results)

    def get_report(self) -> Dict[str, Any]:
        """Get aggregated report.

        Returns:
            Dict containing test statistics.
        """
        total = len(self._results)
        passed = sum(1 for r in self._results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self._results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in self._results if r.status == TestStatus.SKIPPED)
        errors = sum(1 for r in self._results if r.status == TestStatus.ERROR)
        durations = [r.duration_ms for r in self._results]

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "errors": errors,
            "pass_rate": passed / total if total > 0 else 0.0,
            "total_duration_ms": sum(durations),
            "avg_duration_ms": sum(durations) / len(durations) if durations else 0,
        }

    def get_summary(self) -> Dict[str, Any]:
        """Compatibility alias used by some tests."""
        report = self.get_report()
        return {
            "total": report.get("total", 0),
            "passed": report.get("passed", 0),
            "failed": report.get("failed", 0),
            "skipped": report.get("skipped", 0),
            "errors": report.get("errors", 0),
        }

    def get_by_suite(self) -> Dict[str, Dict[str, int]]:
        """Group results by suite prefix ("suite/test")."""
        by_suite: Dict[str, Dict[str, int]] = {}
        for r in self._results:
            suite = "unknown"
            if "/" in r.test_name:
                suite = r.test_name.split("/", 1)[0]
            by_suite.setdefault(suite, {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0})
            by_suite[suite]["total"] += 1
            if r.status == TestStatus.PASSED:
                by_suite[suite]["passed"] += 1
            elif r.status == TestStatus.FAILED:
                by_suite[suite]["failed"] += 1
            elif r.status == TestStatus.SKIPPED:
                by_suite[suite]["skipped"] += 1
            elif r.status == TestStatus.ERROR:
                by_suite[suite]["errors"] += 1
        return by_suite

    def get_failures(self) -> List[TestResult]:
        """Get failed tests."""
        return [r for r in self._results if r.status == TestStatus.FAILED]

    def clear(self) -> None:
        """Clear all results."""
        self._results.clear()


class CoverageTracker:
    """Lightweight coverage hit tracker used by tests."""

    def __init__(self) -> None:
        self._hits: Dict[str, int] = {}
        self._targets: Set[str] = set()

    def register_target(self, name: str) -> None:
        self._targets.add(name)

    def record_hit(self, name: str) -> None:
        self._hits[name] = self._hits.get(name, 0) + 1

    def get_hits(self) -> Dict[str, int]:
        return dict(self._hits)

    def get_percentage(self) -> float:
        if not self._targets:
            return 0.0
        covered = sum(1 for t in self._targets if self._hits.get(t, 0) > 0)
        return (covered / len(self._targets)) * 100.0


# ============================================================================
# Test Assertion Helpers
# ============================================================================
class AgentAssertions:
    """Custom assertion helpers for agent testing.

    Example:
        assertions=AgentAssertions()
        assertions.assert_valid_python("print('hello')")
        assertions.assert_markdown_structure(content, headers=True)
    """

    def __init__(self) -> None:
        """Initialize assertion helpers."""
        self._assertions: List[TestAssertion] = []

    def assert_valid_python(self, code: str) -> bool:
        """Assert code is valid Python.

        Args:
            code: Python code to validate.

        Returns:
            bool: True if valid.

        Raises:
            AssertionError: If invalid Python.
        """
        try:
            compile(code, "<string>", "exec")
            assertion = TestAssertion(
                name="valid_python",
                expected="valid",
                actual="valid",
                passed=True,
            )
            self._assertions.append(assertion)
            return True
        except SyntaxError as e:
            assertion = TestAssertion(
                name="valid_python",
                expected="valid",
                actual=f"invalid: {e}",
                passed=False,
            )
            self._assertions.append(assertion)
            raise AssertionError(f"Invalid Python: {e}")

    def assert_contains_docstring(self, code: str) -> bool:
        """Assert code contains docstrings.

        Args:
            code: Python code to check.

        Returns:
            bool: True if contains docstrings.
        """
        has_docstring = '"""' in code or "'''" in code
        assertion = TestAssertion(
            name="contains_docstring",
            expected=True,
            actual=has_docstring,
            passed=has_docstring,
        )
        self._assertions.append(assertion)

        if not has_docstring:
            raise AssertionError("Code does not contain docstrings")
        return True

    def assert_markdown_structure(
        self,
        content: str,
        headers: bool = True,
        code_blocks: bool = False,
    ) -> bool:
        """Assert markdown has expected structure.

        Args:
            content: Markdown content.
            headers: Expect headers.
            code_blocks: Expect code blocks.

        Returns:
            bool: True if structure matches.
        """
        issues: List[str] = []
        if headers and not re.search(r"^#+\s", content, re.MULTILINE):
            issues.append("missing headers")
        if code_blocks and "```" not in content:
            issues.append("missing code blocks")
        passed = len(issues) == 0
        assertion = TestAssertion(
            name="markdown_structure",
            expected="valid structure",
            actual=", ".join(issues) if issues else "valid",
            passed=passed,
        )
        self._assertions.append(assertion)
        if not passed:
            raise AssertionError(f"Markdown structure issues: {', '.join(issues)}")
        return True

    def assert_json_valid(self, content: str) -> bool:
        """Assert content is valid JSON.

        Args:
            content: JSON content.

        Returns:
            bool: True if valid JSON.
        """
        try:
            json.loads(content)
            assertion = TestAssertion(
                name="json_valid",
                expected="valid",
                actual="valid",
                passed=True,
            )
            self._assertions.append(assertion)
            return True
        except json.JSONDecodeError as e:
            assertion = TestAssertion(
                name="json_valid",
                expected="valid",
                actual=f"invalid: {e}",
                passed=False,
            )
            self._assertions.append(assertion)
            raise AssertionError(f"Invalid JSON: {e}")

    def get_assertions(self) -> List[TestAssertion]:
        """Get all recorded assertions."""
        return list(self._assertions)


# ============================================================================
# Parameterized Test Generator
# ============================================================================
@dataclass
class ParameterizedTestCase:
    """A parameterized test case.

    Attributes:
        name: Test case name.
        params: Parameters for the test.
        expected: Expected result.
        tags: Optional tags for filtering.
    """

    name: str
    params: Dict[str, Any]
    expected: Any
    tags: List[str] = field(default_factory=lambda: [])


class ParameterizedTestGenerator:
    """Generator for parameterized tests.

    Generates test cases from parameter combinations for data - driven testing.

    Example:
        gen=ParameterizedTestGenerator()
        gen.add_parameter("size", [1, 10, 100])
        gen.add_parameter("mode", ["fast", "slow"])
        cases=gen.generate_cases()  # 6 combinations
    """

    def __init__(self, test_name: str = "test") -> None:
        """Initialize generator.

        Args:
            test_name: Base name for generated tests.
        """
        self.test_name = test_name
        self._parameters: Dict[str, List[Any]] = {}
        self._expected_fn: Optional[Callable[..., Any]] = None

    def add_parameter(self, name: str, values: List[Any]) -> "ParameterizedTestGenerator":
        """Add parameter with possible values.

        Args:
            name: Parameter name.
            values: List of possible values.

        Returns:
            Self for chaining.
        """
        self._parameters[name] = values
        return self

    def set_expected_fn(self, fn: Callable[..., Any]) -> "ParameterizedTestGenerator":
        """Set function to compute expected result.

        Args:
            fn: Function that takes params dict and returns expected.

        Returns:
            Self for chaining.
        """
        self._expected_fn = fn
        return self

    def generate_cases(self) -> List[ParameterizedTestCase]:
        """Generate all test case combinations.

        Returns:
            List of parameterized test cases.
        """
        if not self._parameters:
            return []
        import itertools
        keys = list(self._parameters.keys())
        values = [self._parameters[k] for k in keys]
        cases: List[ParameterizedTestCase] = []
        for i, combo in enumerate(itertools.product(*values)):
            params = dict(zip(keys, combo))
            expected = self._expected_fn(params) if self._expected_fn else None
            case = ParameterizedTestCase(
                name=f"{self.test_name}_{i}",
                params=params,
                expected=expected,
            )
            cases.append(case)
        return cases


# ============================================================================
# Test Dependency Injection
# ============================================================================
class DependencyContainer:
    """Container for test dependency injection.

    Manages dependencies for configurable testing with easy mocking.

    Example:
        container=DependencyContainer()
        container.register("db", MockDatabase())
        container.register("api", MockAPI())

        @container.inject
        def test_func(db, api):
            ...
    """

    def __init__(self) -> None:
        """Initialize dependency container."""
        self._dependencies: Dict[str, Any] = {}
        self._factories: Dict[str, Tuple[Callable[[], Any], bool]] = {}
        self._singletons: Dict[str, Any] = {}

    def register(self, name: str, instance: Any) -> None:
        """Register a dependency instance.

        Args:
            name: Dependency name.
            instance: Dependency instance.
        """
        self._dependencies[name] = instance
        logging.debug(f"Registered dependency: {name}")

    def register_factory(
        self,
        name: str,
        factory: Callable[[], Any],
        singleton: bool = False,
    ) -> None:
        """Register a dependency factory.

        Args:
            name: Dependency name.
            factory: Factory function.
            singleton: Whether to create only once.
        """
        self._factories[name] = (factory, singleton)

    def resolve(self, name: str) -> Any:
        """Resolve a dependency.

        Args:
            name: Dependency name.

        Returns:
            Dependency instance.

        Raises:
            KeyError: If dependency not found.
        """
        if name in self._dependencies:
            return self._dependencies[name]
        if name in self._factories:
            factory, singleton = self._factories[name]
            if singleton and name in self._singletons:
                return self._singletons[name]
            instance = factory()
            if singleton:
                self._singletons[name] = instance
            return instance
        raise KeyError(f"Dependency not found: {name}")

    def inject(self, fn: Callable[..., T]) -> Callable[..., T]:
        """Decorator to inject dependencies into function.

        Args:
            fn: Function to inject into.

        Returns:
            Wrapped function with injected dependencies.
        """
        import inspect
        sig = inspect.signature(fn)

        def wrapper(*args: Any, **kwargs: Any) -> T:
            for param in sig.parameters.values():
                if param.name not in kwargs and param.name in self._dependencies:
                    kwargs[param.name] = self.resolve(param.name)
            return fn(*args, **kwargs)
        return wrapper

    def clear(self) -> None:
        """Clear all dependencies."""
        self._dependencies.clear()
        self._factories.clear()
        self._singletons.clear()


# ============================================================================
# Test Flakiness Detection
# ============================================================================
@dataclass
class FlakinessReport:
    """Report of test flakiness analysis.

    Attributes:
        test_name: Name of the test.
        runs: Number of test runs.
        passes: Number of passed runs.
        failures: Number of failed runs.
        flakiness_score: Score from 0 (stable) to 1 (very flaky).
        failure_messages: Unique failure messages.
    """

    test_name: str
    runs: int
    passes: int
    failures: int
    flakiness_score: float
    failure_messages: List[str] = field(default_factory=lambda: [])


class FlakinessDetector:
    """Detects flaky tests through repeated execution.

    Runs tests multiple times to identify intermittent failures.

    Example:
        detector=FlakinessDetector()
        report=detector.analyze(test_fn, runs=10)
        if report.flakiness_score > 0.1:
            print(f"Test is flaky: {report.flakiness_score}")
    """

    def __init__(self, default_runs: int = 5) -> None:
        """Initialize detector.

        Args:
            default_runs: Default number of test runs.
        """
        self.default_runs = default_runs
        self._history: Dict[str, List[FlakinessReport]] = {}

    def analyze(
        self,
        test_fn: Callable[[], None],
        runs: Optional[int] = None,
        test_name: Optional[str] = None,
    ) -> FlakinessReport:
        """Analyze test for flakiness.

        Args:
            test_fn: Test function to analyze.
            runs: Number of runs.
            test_name: Test name for reporting.

        Returns:
            FlakinessReport with analysis results.
        """
        runs = runs or self.default_runs
        test_name = test_name or test_fn.__name__

        passes = 0
        failures = 0
        failure_messages: List[str] = []

        for _ in range(runs):
            try:
                test_fn()
                passes += 1
            except Exception as e:
                failures += 1
                msg = str(e)
                if msg not in failure_messages:
                    failure_messages.append(msg)

        # Calculate flakiness score
        # 0=all same result, 1=50 / 50 split
        if runs > 0:
            p = passes / runs
            flakiness = 1 - abs(2 * p - 1)  # 0 at 0% or 100%, 1 at 50%
        else:
            flakiness = 0.0

        report = FlakinessReport(
            test_name=test_name,
            runs=runs,
            passes=passes,
            failures=failures,
            flakiness_score=flakiness,
            failure_messages=failure_messages,
        )

        # Store in history
        if test_name not in self._history:
            self._history[test_name] = []
        self._history[test_name].append(report)

        return report

    def get_history(self, test_name: str) -> List[FlakinessReport]:
        """Get flakiness history for a test."""
        return self._history.get(test_name, [])

    def get_flaky_tests(self, threshold: float = 0.1) -> List[str]:
        """Get tests that exceed flakiness threshold."""
        flaky: List[str] = []
        for name, reports in self._history.items():
            if reports and reports[-1].flakiness_score > threshold:
                flaky.append(name)
        return flaky


# ============================================================================
# Test Data Cleanup Utilities
# ============================================================================
class TestDataCleaner:
    """Utilities for cleaning up test data.

    Manages cleanup of test artifacts with configurable strategies.

    Example:
        cleaner=TestDataCleaner()
        cleaner.register_path(temp_dir)
        cleaner.register_file(temp_file)
        cleaner.cleanup_all()
    """

    def __init__(self, strategy: CleanupStrategy = CleanupStrategy.IMMEDIATE) -> None:
        """Initialize cleaner.

        Args:
            strategy: Default cleanup strategy.
        """
        self.strategy = strategy
        self._paths: List[Tuple[Path, bool]] = []
        self._files: List[Path] = []
        self._callbacks: List[Callable[[], None]] = []
        self._cleanup_done = False

    def register_path(self, path: Path, recursive: bool = True) -> None:
        """Register directory for cleanup.

        Args:
            path: Directory path.
            recursive: Whether to remove recursively.
        """
        self._paths.append((path, recursive))

    def register_file(self, path: Path) -> None:
        """Register file for cleanup.

        Args:
            path: File path.
        """
        self._files.append(path)

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register cleanup callback.

        Args:
            callback: Function to call during cleanup.
        """
        self._callbacks.append(callback)

    def cleanup_all(self, force: bool = False) -> int:
        """Clean up all registered resources.

        Args:
            force: Force cleanup regardless of strategy.

        Returns:
            Number of items cleaned.
        """
        if self._cleanup_done and not force:
            return 0

        cleaned = 0

        # Clean files
        for file_path in self._files:
            try:
                if file_path.exists():
                    file_path.unlink()
                    cleaned += 1
            except OSError as e:
                logging.warning(f"Failed to clean file {file_path}: {e}")

        # Clean directories
        for path, recursive in self._paths:
            try:
                if path.exists():
                    if recursive:
                        shutil.rmtree(path)
                    else:
                        path.rmdir()
                    cleaned += 1
            except OSError as e:
                logging.warning(f"Failed to clean path {path}: {e}")

        # Run callbacks
        for callback in self._callbacks:
            try:
                callback()
                cleaned += 1
            except Exception as e:
                logging.warning(f"Cleanup callback failed: {e}")

        self._cleanup_done = True
        return cleaned

    def __enter__(self) -> "TestDataCleaner":
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit - perform cleanup."""
        if self.strategy == CleanupStrategy.IMMEDIATE:
            self.cleanup_all()


# ============================================================================
# Cross - Platform Test Helpers
# ============================================================================
class CrossPlatformHelper:
    """Helpers for cross-platform testing.

    Provides utilities to handle platform differences in tests.

    Example:
        helper=CrossPlatformHelper()
        path=helper.normalize_path("/some / path")
        if helper.is_windows():
            # Windows - specific test code
    """

    def __init__(self) -> None:
        """Initialize helper."""
        self._platform = sys.platform

    def is_windows(self) -> bool:
        """Check if running on Windows."""
        return self._platform.startswith("win")

    def is_linux(self) -> bool:
        """Check if running on Linux."""
        return self._platform.startswith("linux")

    def is_macos(self) -> bool:
        """Check if running on macOS."""
        return self._platform == "darwin"

    def normalize_path(self, path: str) -> Path:
        """Normalize path for current platform.

        Args:
            path: Path string.

        Returns:
            Normalized Path object.
        """
        return Path(path).resolve()

    def normalize_line_endings(self, content: str) -> str:
        """Normalize line endings to platform default.

        Args:
            content: Text content.

        Returns:
            Content with normalized line endings.
        """
        # First normalize to \n, then to platform default
        normalized = content.replace("\r\n", "\n").replace("\r", "\n")
        if self.is_windows():
            return normalized.replace("\n", "\r\n")
        return normalized

    def get_temp_dir(self) -> Path:
        """Get platform-appropriate temp directory."""
        return Path(tempfile.gettempdir())

    def skip_on_platform(self, *platforms: str) -> bool:
        """Check if test should be skipped on current platform.

        Args:
            platforms: Platform names to skip ("windows", "linux", "macos").

        Returns:
            True if should skip.
        """
        platform_map = {
            "windows": self.is_windows(),
            "linux": self.is_linux(),
            "macos": self.is_macos(),
        }
        return any(platform_map.get(p, False) for p in platforms)


# ============================================================================
# Test Logging and Debugging
# ============================================================================
@dataclass
class TestLogEntry:
    """A test log entry.

    Attributes:
        level: Log level.
        message: Log message.
        timestamp: When logged.
        test_name: Associated test.
        extra: Extra data.
    """

    level: str
    message: str
    timestamp: float = field(default_factory=time.time)
    test_name: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=lambda: {})


class TestLogger:
    """Logger for test debugging.

    Captures logs during test execution for debugging.

    Example:
        logger=TestLogger()
        with logger.capture("test_name"):
            logger.info("Test started")
            # ... test code ...
        logs=logger.get_logs("test_name")
    """

    def __init__(self) -> None:
        """Initialize logger."""
        self._logs: Dict[str, List[TestLogEntry]] = {}
        self._current_test: Optional[str] = None

    def _log(self, level: str, message: str, **extra: Any) -> None:
        """Internal log method."""
        entry = TestLogEntry(
            level=level,
            message=message,
            test_name=self._current_test,
            extra=extra,
        )

        if self._current_test:
            if self._current_test not in self._logs:
                self._logs[self._current_test] = []
            self._logs[self._current_test].append(entry)

    def debug(self, message: str, **extra: Any) -> None:
        """Log debug message."""
        self._log("DEBUG", message, **extra)

    def info(self, message: str, **extra: Any) -> None:
        """Log info message."""
        self._log("INFO", message, **extra)

    def warning(self, message: str, **extra: Any) -> None:
        """Log warning message."""
        self._log("WARNING", message, **extra)

    def error(self, message: str, **extra: Any) -> None:
        """Log error message."""
        self._log("ERROR", message, **extra)

    @contextmanager
    def capture(self, test_name: str) -> Iterator["TestLogger"]:
        """Context manager to capture logs for a test.

        Args:
            test_name: Name of the test.

        Yields:
            Self for logging.
        """
        old_test = self._current_test
        self._current_test = test_name
        self._logs[test_name] = []
        try:
            yield self
        finally:
            self._current_test = old_test

    def get_logs(self, test_name: str) -> List[TestLogEntry]:
        """Get logs for a test."""
        return self._logs.get(test_name, [])

    def get_errors(self, test_name: str) -> List[TestLogEntry]:
        """Get error logs for a test."""
        return [entry for entry in self.get_logs(test_name) if entry.level == "ERROR"]

    def clear(self) -> None:
        """Clear all logs."""
        self._logs.clear()


# ============================================================================
# Test Parallelization Helpers
# ============================================================================
@dataclass
class ParallelTestResult:
    """Result from parallel test execution.

    Attributes:
        test_name: Name of the test.
        passed: Whether test passed.
        duration_ms: Test duration.
        error: Error if failed.
        worker_id: Worker that ran the test.
    """

    test_name: str
    passed: bool
    duration_ms: float
    error: Optional[str] = None
    worker_id: int = 0


class ParallelTestRunner:
    """Helper for parallel test execution.

    Manages parallel execution of tests with worker pools.

    Example:
        runner=ParallelTestRunner(workers=4)
        runner.add_test("test1", test_func1)
        runner.add_test("test2", test_func2)
        results=runner.run_all()
    """

    def __init__(self, workers: int = 4) -> None:
        """Initialize runner.

        Args:
            workers: Number of worker threads.
        """
        self.workers = workers
        self._tests: Dict[str, Callable[[], None]] = {}
        self._results: List[ParallelTestResult] = []
        self.success_count = 0
        self.failure_count = 0

    def add_test(self, name: str, test_fn: Callable[[], None]) -> None:
        """Add test to run.

        Args:
            name: Test name.
            test_fn: Test function.
        """
        self._tests[name] = test_fn

    def run(self, test_functions: List[Callable[[], Any]], fail_fast: bool = True) -> List[Any]:
        """Run tests in parallel.

        Args:
            test_functions: List of test functions to run.
            fail_fast: Stop on first failure.

        Returns:
            List of results from test functions.
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
        self.success_count = 0
        self.failure_count = 0
        results: List[Any] = []
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {executor.submit(test_fn): i for i, test_fn in enumerate(test_functions)}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    self.success_count += 1
                except Exception:
                    self.failure_count += 1
                    if fail_fast:
                        executor.shutdown(wait=False)
                        raise
                    results.append(None)
        return results

    def _run_test(
        self,
        name: str,
        test_fn: Callable[[], None],
        worker_id: int,
    ) -> ParallelTestResult:
        """Run a single test."""
        start = time.time()
        try:
            test_fn()
            return ParallelTestResult(
                test_name=name,
                passed=True,
                duration_ms=(time.time() - start) * 1000,
                worker_id=worker_id,
            )
        except Exception as e:
            return ParallelTestResult(
                test_name=name,
                passed=False,
                duration_ms=(time.time() - start) * 1000,
                error=str(e),
                worker_id=worker_id,
            )

    def run_all(self) -> List[ParallelTestResult]:
        """Run all tests in parallel.

        Returns:
            List of test results.
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed, Future

        self._results = []

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures: Dict[Future[ParallelTestResult], str] = {}
            for i, (name, test_fn) in enumerate(self._tests.items()):
                worker_id = i % self.workers
                future = executor.submit(self._run_test, name, test_fn, worker_id)
                futures[future] = name

            for future in as_completed(futures):
                result: ParallelTestResult = future.result()
                self._results.append(result)

        return self._results

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of parallel test execution."""
        total = len(self._results)
        passed = sum(1 for r in self._results if r.passed)
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "total_duration_ms": sum(r.duration_ms for r in self._results),
        }


# ============================================================================
# Test Recording and Replay
# ============================================================================
@dataclass
class RecordedInteraction:
    """A recorded test interaction.

    Attributes:
        call_type: Type of call (e.g., "api", "file", "db").
        call_name: Name of the call.
        args: Call arguments.
        kwargs: Call keyword arguments.
        result: Call result.
        timestamp: When recorded.
    """

    call_type: str
    call_name: str
    args: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = field(default_factory=lambda: {})
    result: Any = None
    timestamp: float = field(default_factory=time.time)


class TestRecorder:
    """Records and replays test interactions.

    Useful for recording external calls and replaying in tests.

    Example:
        recorder=TestRecorder()

        # Recording mode
        with recorder.record():
            result=api_call("data")  # Records the call
        recorder.save("test_recording.json")

        # Replay mode
        recorder.load("test_recording.json")
        with recorder.replay():
            result=api_call("data")  # Returns recorded result
    """

    def __init__(self) -> None:
        """Initialize recorder."""
        self._recordings: List[RecordedInteraction] = []
        self._replay_index = 0
        self._mode: str = "normal"  # "record", "replay", "normal"

    def record_interaction(
        self,
        call_type: str,
        call_name: str,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
        result: Any,
    ) -> None:
        """Record an interaction.

        Args:
            call_type: Type of call.
            call_name: Name of the call.
            args: Arguments.
            kwargs: Keyword arguments.
            result: Result of the call.
        """
        if self._mode == "record":
            interaction = RecordedInteraction(
                call_type=call_type,
                call_name=call_name,
                args=args,
                kwargs=kwargs,
                result=result,
            )
            self._recordings.append(interaction)

    def get_replay_result(
        self,
        call_type: str,
        call_name: str,
    ) -> Optional[Any]:
        """Get replayed result for a call.

        Args:
            call_type: Type of call.
            call_name: Name of the call.

        Returns:
            Recorded result or None.
        """
        if self._mode != "replay":
            return None

        if self._replay_index < len(self._recordings):
            recording = self._recordings[self._replay_index]
            if recording.call_type == call_type and recording.call_name == call_name:
                self._replay_index += 1
                return recording.result

        return None

    @contextmanager
    def record(self) -> Iterator["TestRecorder"]:
        """Context manager for recording mode."""
        self._mode = "record"
        self._recordings = []
        try:
            yield self
        finally:
            self._mode = "normal"

    @contextmanager
    def replay(self) -> Iterator["TestRecorder"]:
        """Context manager for replay mode."""
        self._mode = "replay"
        self._replay_index = 0
        try:
            yield self
        finally:
            self._mode = "normal"

    def save(self, path: Path) -> None:
        """Save recordings to file."""
        data: List[Dict[str, Any]] = []
        for r in self._recordings:
            data.append({
                "call_type": r.call_type,
                "call_name": r.call_name,
                "args": list(r.args),
                "kwargs": r.kwargs,
                "result": r.result,
                "timestamp": r.timestamp,
            })
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def load(self, path: Path) -> None:
        """Load recordings from file."""
        with open(path) as f:
            data = json.load(f)
        self._recordings = [
            RecordedInteraction(
                call_type=d["call_type"],
                call_name=d["call_name"],
                args=tuple(d["args"]),
                kwargs=d["kwargs"],
                result=d["result"],
                timestamp=d["timestamp"],
            )
            for d in data
        ]


# ============================================================================
# Test Baseline Management
# ============================================================================
@dataclass
class TestBaseline:
    """A test baseline for comparison.

    Attributes:
        name: Baseline name.
        values: Baseline values.
        created_at: Creation timestamp.
        version: Baseline version.
    """

    name: str
    values: Dict[str, Any]
    created_at: float = field(default_factory=time.time)
    version: int = 1


class BaselineManager:
    """Manages test baselines for comparison.

    Stores and compares baselines for regression testing.

    Example:
        manager=BaselineManager(baseline_dir)
        manager.save_baseline("perf", {"latency": 100, "memory": 50})

        # Later...
        baseline=manager.load_baseline("perf")
        diff=manager.compare("perf", {"latency": 120, "memory": 50})
    """

    def __init__(self, baseline_dir: Path) -> None:
        """Initialize manager.

        Args:
            baseline_dir: Directory for baseline files.
        """
        self.baseline_dir = baseline_dir
        self.baseline_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, name: str) -> Path:
        """Get path for baseline file."""
        return self.baseline_dir / f"{name}.baseline.json"

    def save_baseline(self, name: str, values: Dict[str, Any]) -> TestBaseline:
        """Save a baseline.

        Args:
            name: Baseline name.
            values: Baseline values.

        Returns:
            Created baseline.
        """
        existing = self.load_baseline(name)
        version = existing.version + 1 if existing else 1

        baseline = TestBaseline(name=name, values=values, version=version)

        with open(self._get_path(name), "w") as f:
            json.dump({
                "name": baseline.name,
                "values": baseline.values,
                "created_at": baseline.created_at,
                "version": baseline.version,
            }, f, indent=2)

        return baseline

    def load_baseline(self, name: str) -> Optional[TestBaseline]:
        """Load a baseline.

        Args:
            name: Baseline name.

        Returns:
            Loaded baseline or None.
        """
        path = self._get_path(name)
        if not path.exists():
            return None

        with open(path) as f:
            data = json.load(f)

        return TestBaseline(
            name=data["name"],
            values=data["values"],
            created_at=data["created_at"],
            version=data["version"],
        )

    def compare(
        self,
        name: str,
        current: Dict[str, Any],
        tolerance: float = 0.1,
    ) -> Dict[str, Any]:
        """Compare current values against baseline.

        Args:
            name: Baseline name.
            current: Current values.
            tolerance: Tolerance for numeric comparisons (0.1=10%).

        Returns:
            Comparison results with diffs.
        """
        baseline = self.load_baseline(name)
        if not baseline:
            return {"error": "no baseline"}

        diffs = {}
        for key, current_val in current.items():
            if key not in baseline.values:
                diffs[key] = {"status": "new", "current": current_val}
                continue

            baseline_val = baseline.values[key]

            if isinstance(current_val, (int, float)) and isinstance(baseline_val, (int, float)):
                if baseline_val == 0:
                    pct_change = float("inf") if current_val != 0 else 0
                else:
                    pct_change = abs(current_val - baseline_val) / abs(baseline_val)

                if pct_change > tolerance:
                    diffs[key] = {
                        "status": "changed",
                        "baseline": baseline_val,
                        "current": current_val,
                        "pct_change": pct_change,
                    }
            elif current_val != baseline_val:
                diffs[key] = {
                    "status": "changed",
                    "baseline": baseline_val,
                    "current": current_val,
                }

        return {
            "baseline_version": baseline.version,
            "diffs": diffs,
            "passed": len(diffs) == 0,  # type: ignore[arg-type]
        }


# ============================================================================
# Test Configuration Profiles
# ============================================================================
@dataclass
class TestProfile:
    """A test configuration profile.

    Attributes:
        name: Profile name.
        settings: Profile settings.
        env_vars: Environment variables.
        enabled: Whether profile is enabled.
    """

    name: str
    settings: Dict[str, Any] = field(default_factory=lambda: {})
    env_vars: Dict[str, str] = field(default_factory=lambda: {})
    enabled: bool = True


class TestProfileManager:
    """Manages test configuration profiles.

    Allows switching between test configurations easily.

    Example:
        manager=TestProfileManager()
        manager.add_profile(TestProfile("ci", settings={"timeout": 60}))
        manager.add_profile(TestProfile("local", settings={"timeout": 300}))

        manager.activate("ci")
        timeout=manager.get_setting("timeout")  # 60
    """

    def __init__(self) -> None:
        """Initialize profile manager."""
        self._profiles: Dict[str, TestProfile] = {}
        self._active: Optional[str] = None
        self._original_env: Dict[str, Optional[str]] = {}

    def add_profile(self, profile: TestProfile) -> None:
        """Add a profile.

        Args:
            profile: Profile to add.
        """
        self._profiles[profile.name] = profile

    def get_profile(self, name: str) -> Optional[TestProfile]:
        """Get a profile by name."""
        return self._profiles.get(name)

    def activate(self, name: str) -> None:
        """Activate a profile.

        Args:
            name: Profile name.

        Raises:
            KeyError: If profile not found.
        """
        if name not in self._profiles:
            raise KeyError(f"Profile not found: {name}")

        # Deactivate current
        if self._active:
            self.deactivate()

        profile = self._profiles[name]

        # Set environment variables
        for key, value in profile.env_vars.items():
            self._original_env[key] = os.environ.get(key)
            os.environ[key] = value

        self._active = name
        logging.info(f"Activated test profile: {name}")

    def deactivate(self) -> None:
        """Deactivate current profile."""
        if not self._active:
            return

        # Restore environment
        for key, value in self._original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

        self._original_env.clear()
        self._active = None

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get setting from active profile.

        Args:
            key: Setting key.
            default: Default value.

        Returns:
            Setting value.
        """
        if not self._active:
            return default

        profile = self._profiles[self._active]
        return profile.settings.get(key, default)

    def get_active_profile(self) -> Optional[TestProfile]:
        """Get currently active profile."""
        if self._active:
            return self._profiles[self._active]
        return None


# ============================================================================
# Legacy Functions (Preserved)
# ============================================================================
@contextmanager
def agent_dir_on_path() -> Iterator[None]:
    """Temporarily add the agent directory to sys.path.

    Note: This is a legacy helper to support tests that rely on implicit imports
    from the scripts / agent directory. For new code, prefer using load_agent_module
    or proper package imports.
    """
    old_sys_path = list(sys.path)
    sys.path.insert(0, str(AGENT_DIR))
    try:
        yield
    finally:
        sys.path[:] = old_sys_path


# ========== Additional Test Utilities Classes ==========
class EnvironmentDetector:
    """Detects and reports test environment information."""

    def detect(self) -> Dict[str, Any]:
        """Detect environment information."""
        import platform
        import os
        is_ci = any(
            env in os.environ
            for env in ['CI', 'CONTINUOUS_INTEGRATION', 'BUILD_ID', 'GITHUB_ACTIONS']
        )
        system = platform.system().lower()
        if system == 'windows':
            os_name = 'windows'
        elif system == 'darwin':
            os_name = 'darwin'
        elif system == 'linux':
            os_name = 'linux'
        else:
            os_name = 'unknown'
        return {
            'is_ci': is_ci,
            'os': os_name,
            'python_version': platform.python_version(),
            'platform': system
        }


class LogCapturer:
    """Captures logging output for testing."""

    def __init__(self, level: int = logging.INFO) -> None:
        """Initialize log capturer."""
        self.level = level
        self.logs: List[logging.LogRecord] = []
        self.handler = logging.Handler()
        self.handler.emit = lambda record: self.logs.append(record)

    def __enter__(self) -> "LogCapturer":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.stop()

    def start(self) -> None:
        """Start capturing logs."""
        root_logger = logging.getLogger()
        root_logger.addHandler(self.handler)
        root_logger.setLevel(self.level)

    def stop(self) -> None:
        """Stop capturing logs."""
        logging.getLogger().removeHandler(self.handler)

    def get_logs(self, level: Optional[int] = None) -> List[str]:
        """Get captured log messages."""
        if level is None:
            return [record.getMessage() for record in self.logs]
        return [record.getMessage() for record in self.logs if record.levelno >= level]


class TestConfigLoader:
    """Loads test configuration from files."""

    def __init__(self, config_path: Optional[Path] = None) -> None:
        """Initialize config loader."""
        self.config_path = config_path or Path("test_config.json")
        self.config: Dict[str, Any] = {}

    def load(self, path: Optional[Path] = None, defaults: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Load configuration.

        Compatibility:
        - Tests pass a `Path` to load.
        - Tests may pass `defaults=` to be merged.
        """
        if path is not None:
            self.config_path = Path(path)

        loaded: Dict[str, Any] = {}
        if self.config_path.exists():
            with open(self.config_path, encoding="utf-8") as f:
                loaded = json.load(f)

        if defaults:
            merged = dict(defaults)
            merged.update(loaded)
            self.config = merged
        else:
            self.config = loaded

        return self.config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)


class TestReportGenerator:
    """Generates test reports in various formats."""

    def __init__(self, output_dir: Optional[Union[str, Path]] = None) -> None:
        """Initialize report generator."""
        self.output_dir = Path(output_dir) if output_dir is not None else None
        if self.output_dir is not None:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: List[Dict[str, Any]] = []

    def add_result(self, test_name: str, passed: bool, duration_ms: float) -> None:
        """Add test result (legacy API)."""
        self.results.append({
            "test_name": test_name,
            "status": "passed" if passed else "failed",
            "duration_ms": float(duration_ms),
        })

    def add_test_result(self, test_name: str, status: str, duration_ms: float, error: str = "") -> None:
        """Add test result (test compatibility API)."""
        self.results.append({
            "test_name": test_name,
            "status": status,
            "duration_ms": float(duration_ms),
            "error": error,
        })

    def _render_html(self) -> str:
        rows = ""
        for r in self.results:
            status = str(r.get("status", ""))
            duration = float(r.get("duration_ms", 0.0))
            error = str(r.get("error", ""))
            rows += (
                f"<tr><td>{r.get('test_name', '')}</td><td>{status}</td><td>{duration:.2f}ms</td>"
                f"<td>{error}</td></tr>"
            )
        return (
            "<html><head><title>Test Report</title></head><body>"
            "<h1>Test Results</h1>"
            "<table border=\"1\">"
            "<tr><th>Test</th><th>Status</th><th>Duration</th><th>Error</th></tr>"
            f"{rows}</table></body></html>"
        )

    def generate_html(self) -> Path:
        """Generate HTML report file."""
        if self.output_dir is None:
            self.output_dir = Path.cwd()
        path = self.output_dir / "test_report.html"
        path.write_text(self._render_html(), encoding="utf-8")
        return path

    def generate_json(self) -> Path:
        """Generate JSON report file."""
        if self.output_dir is None:
            self.output_dir = Path.cwd()
        path = self.output_dir / "test_report.json"
        payload = {"results": self.results}
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path


class CleanupManager:
    """Manages cleanup hooks for tests."""

    def __init__(self) -> None:
        """Initialize cleanup manager."""
        self.hooks: List[Callable[[], None]] = []

    def add_hook(self, hook: Callable[[], None]) -> None:
        """Add cleanup hook."""
        self.hooks.append(hook)

    def register(self, hook: Callable[[], None]) -> None:
        """Compatibility alias for add_hook."""
        self.add_hook(hook)

    def cleanup(self) -> None:
        """Execute all cleanup hooks."""
        for hook in reversed(self.hooks):
            try:
                hook()
            except Exception:
                pass


class DependencyResolver:
    """Resolves dependencies between tests."""

    def __init__(self) -> None:
        """Initialize resolver."""
        self.dependencies: Dict[str, List[str]] = {}

    def add_test(self, name: str, depends_on: List[str]) -> None:
        """Register a test and its dependencies (test compatibility API)."""
        self.dependencies[name] = list(depends_on)

    def add_dependency(self, test: str, depends_on: str) -> None:
        """Add dependency."""
        if test not in self.dependencies:
            self.dependencies[test] = []
        self.dependencies[test].append(depends_on)

    def resolve(self) -> List[str]:
        """Resolve execution order or raise on circular dependencies."""
        visiting: Set[str] = set()
        visited: Set[str] = set()
        order: List[str] = []

        def visit(node: str) -> None:
            if node in visited:
                return
            if node in visiting:
                raise ValueError("Circular dependency detected")
            visiting.add(node)
            for dep in self.dependencies.get(node, []):
                visit(dep)
            visiting.remove(node)
            visited.add(node)
            order.append(node)

        nodes: Set[str] = set(self.dependencies.keys())
        for deps in self.dependencies.values():
            nodes.update(deps)
        for n in sorted(nodes):
            visit(n)
        return order

    def resolve_order(self) -> List[str]:
        """Resolve execution order (topological sort)."""
        visited: Set[str] = set()
        order: List[str] = []

        def visit(node: str) -> None:
            if node in visited:
                return
            visited.add(node)
            for dep in self.dependencies.get(node, []):
                visit(dep)
            order.append(node)

        for test in self.dependencies:
            visit(test)
        return order

    def detect_cycle(self) -> bool:
        """Detect circular dependencies."""
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for dep in self.dependencies.get(node, []):
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for test in self.dependencies:
            if test not in visited:
                if has_cycle(test):
                    return True
        return False


@dataclass(frozen=True)
class ResourceHandle:
    """A handle representing an acquired resource from ResourcePool."""

    name: str


class ResourcePool:
    """Manages resource allocation for tests."""

    def __init__(self, max_resources: int = 10) -> None:
        """Initialize resource pool."""
        self.max_resources = max_resources
        self.available = max_resources
        self.lock = threading.Lock()
        self._allocations: Dict[str, int] = {}

    def acquire(self, count: Union[int, str] = 1, timeout: float = 10.0) -> Optional[ResourceHandle]:
        """Acquire a resource.

        Compatibility:
        - Tests call `acquire("test_name", timeout=...)` and expect a handle or None.
        - Legacy code may call `acquire(count)`.
        """
        if isinstance(count, str):
            name = count
            start = time.time()
            while time.time() - start < timeout:
                with self.lock:
                    if self.available >= 1:
                        self.available -= 1
                        self._allocations[name] = self._allocations.get(name, 0) + 1
                        return ResourceHandle(name=name)
                time.sleep(0.01)
            return None

        with self.lock:
            if self.available >= int(count):
                self.available -= int(count)
                return ResourceHandle(name=f"count:{int(count)}")
            return None

    def release(self, handle: Union[int, ResourceHandle] = 1) -> None:
        """Release resources."""
        with self.lock:
            if isinstance(handle, ResourceHandle):
                self.available = min(self.available + 1, self.max_resources)
                self._allocations[handle.name] = max(0, self._allocations.get(handle.name, 0) - 1)
                return
            self.available = min(self.available + int(handle), self.max_resources)

    def wait_available(self, count: int = 1, timeout: float = 10.0) -> bool:
        """Wait for resources to be available."""
        import time as time_module
        start = time_module.time()
        while time_module.time() - start < timeout:
            if self.acquire(count) is not None:
                return True
            time_module.sleep(0.1)
        return False


class EnvironmentIsolator:
    """Context manager that restores environment variables on exit."""

    def __init__(self) -> None:
        self._original: Dict[str, str] = {}

    def __enter__(self) -> "EnvironmentIsolator":
        self._original = dict(os.environ)
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        os.environ.clear()
        os.environ.update(self._original)

    def set_env(self, key: str, value: str) -> None:
        os.environ[str(key)] = str(value)


class RetryHelper:
    """Simple retry helper for flaky operations."""

    def __init__(self, max_retries: int = 3, delay_seconds: float = 0.0) -> None:
        self.max_retries = int(max_retries)
        self.delay_seconds = float(delay_seconds)

    def retry(self, fn: Callable[[], T]) -> T:
        last_exc: Optional[BaseException] = None
        for attempt in range(self.max_retries):
            try:
                return fn()
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if attempt == self.max_retries - 1:
                    raise
                if self.delay_seconds > 0:
                    time.sleep(self.delay_seconds)
        if last_exc is not None:
            raise last_exc
        raise RuntimeError("RetryHelper failed without exception")


def get_base_agent_module() -> ModuleType:
    """Load base_agent module without modifying sys.path."""
    return load_agent_module("base_agent.py", "base_agent")


def load_module_from_path(name: str, path: Path) -> ModuleType:
    """Load a module from a specific path."""
    logging.debug(f"Loading module {name} from {path}")
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        logging.error(f"Could not load module {name} from {path}")
        raise ImportError(f"Could not load module {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@contextmanager
def agent_sys_path() -> Iterator[None]:
    """Add scripts / agent to sys.path temporarily."""
    path = str(AGENT_DIR)
    if path not in sys.path:
        sys.path.insert(0, path)
        try:
            yield
        finally:
            sys.path.remove(path)
    else:
        yield


def load_agent_module(filename: str, module_name: str | None = None) -> ModuleType:
    """Load an agent module from scripts / agent by filename.

    Supports files that are not valid Python identifiers (e.g. `agent - changes.py`).
    """
    path = AGENT_DIR / filename
    if not path.exists():
        raise FileNotFoundError(path)
    if module_name is None:
        safe = re.sub(r"[^0-9a-zA-Z_]+", "_", path.stem)
        if not safe or safe[0].isdigit():
            safe = f"m_{safe}"
        module_name = f"_dv_legacy_{safe}"
    # Use the helper for consistency
    try:
        return load_module_from_path(module_name, path)
    except Exception:
        # Clean up if execution fails
        sys.modules.pop(module_name, None)
        raise
