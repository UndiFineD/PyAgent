#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");

"""Data models for test agent functionality."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from .enums import TestPriority, TestStatus, CoverageType, BrowserType, TestSourceType, MutationOperator


def _empty_str_list() -> List[str]:
    return []


def _empty_dict_any() -> Dict[str, Any]:
    return {}


def _empty_dict_str_status() -> Dict[str, TestStatus]:
    return {}


def _empty_action_list() -> List[Dict[str, Any]]:
    return []


@dataclass
class TestCase:
    """Represents a single test case."""
    __test__ = False
    id: str
    name: str
    file_path: str
    line_number: int
    priority: TestPriority = TestPriority.MEDIUM
    status: TestStatus = TestStatus.PASSED
    duration_ms: float = 0.0
    flakiness_score: float = 0.0
    last_run: str = ""
    run_count: int = 0
    failure_count: int = 0
    tags: List[str] = field(default_factory=lambda: [])
    dependencies: List[str] = field(default_factory=lambda: [])


@dataclass
class TestRun:
    """A test execution run."""
    id: str
    timestamp: str
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    duration_ms: float = 0.0
    test_results: Dict[str, TestStatus] = field(default_factory=lambda: {})


@dataclass
class CoverageGap:
    """Represents a gap in test coverage."""
    file_path: str
    line_start: int
    line_end: int
    coverage_type: CoverageType
    suggestion: str = ""


@dataclass
class TestFactory:
    """A test data factory for generating test data."""
    name: str
    return_type: str
    parameters: Dict[str, str] = field(default_factory=lambda: {})
    generator: str = ""  # Code snippet or function name


@dataclass
class VisualRegressionConfig:
    """Configuration for visual regression testing."""
    baseline_dir: str
    diff_threshold: float = 0.01
    browsers: List[BrowserType] = field(default_factory=lambda: [BrowserType.CHROME])
    viewport_sizes: List[Tuple[int, int]] = field(default_factory=lambda: [(1920, 1080)])
    ignore_regions: List[Tuple[int, int, int, int]] = field(default_factory=lambda: [])


@dataclass
class ContractTest:
    """A contract test for API boundaries."""
    consumer: str
    provider: str
    endpoint: str
    request_schema: Dict[str, Any] = field(default_factory=lambda: {})
    response_schema: Dict[str, Any] = field(default_factory=lambda: {})
    status_code: int = 200


@dataclass
class TestEnvironment:
    """Test environment configuration."""
    name: str
    base_url: str = ""
    variables: Dict[str, str] = field(default_factory=lambda: {})
    fixtures: List[str] = field(default_factory=lambda: [])
    setup_commands: List[str] = field(default_factory=lambda: [])
    teardown_commands: List[str] = field(default_factory=lambda: [])


@dataclass
class ExecutionTrace:
    """Test execution trace for replay."""
    test_id: str
    timestamp: str
    steps: List[Dict[str, Any]] = field(default_factory=lambda: [])
    variables: Dict[str, Any] = field(default_factory=lambda: {})
    stdout: str = ""
    stderr: str = ""


@dataclass
class TestDependency:
    """A dependency for test injection."""
    name: str
    dependency_type: str
    implementation: str = ""
    mock_behavior: str = ""


@dataclass
class CrossBrowserConfig:
    """Cross-browser testing configuration."""
    browsers: List[BrowserType]
    parallel: bool = True
    headless: bool = True
    timeout_seconds: int = 30
    retries: int = 1


@dataclass
class AggregatedResult:
    """Aggregated test result from multiple sources."""
    source: TestSourceType
    test_name: str
    status: TestStatus
    duration_ms: float
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=lambda: {})


@dataclass
class Mutation:
    """A code mutation for mutation testing."""
    id: str
    file_path: str
    line_number: int
    operator: MutationOperator
    original_code: str
    mutated_code: str
    killed: bool = False


@dataclass
class GeneratedTest:
    """A test generated from specification."""
    name: str
    specification: str
    generated_code: str
    confidence: float = 0.0
    validated: bool = False


@dataclass
class TestProfile:
    """Runtime profiling data for a test."""
    test_id: str
    cpu_time_ms: float
    memory_peak_mb: float
    io_operations: int
    function_calls: int
    timestamp: str = ""


@dataclass
class ScheduleSlot:
    """A scheduled time slot for test execution."""
    start_time: str
    end_time: str
    tests: List[str] = field(default_factory=lambda: [])
    workers: int = 1
    priority: TestPriority = TestPriority.MEDIUM


@dataclass
class ProvisionedEnvironment:
    """A provisioned test environment."""
    status: str
    python_version: str = ""
    dependencies: List[str] = field(default_factory=lambda: [])
    config: Dict[str, Any] = field(default_factory=lambda: {})


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    valid: bool
    errors: List[str] = field(default_factory=lambda: [])


@dataclass
class Recording:
    """A recording of test execution."""
    test_name: str
    actions: List[Dict[str, Any]] = field(default_factory=lambda: [])


@dataclass
class ReplayResult:
    """Result of replaying a recorded test."""
    success: bool
    errors: List[str] = field(default_factory=lambda: [])
