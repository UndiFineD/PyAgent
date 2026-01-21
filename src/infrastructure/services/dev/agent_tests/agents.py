# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import ast
import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from src.core.base.lifecycle.base_agent import BaseAgent
from src.infrastructure.services.dev.agent_tests.enums import (
    TestPriority,
    TestStatus,
    CoverageType,
)
from src.infrastructure.services.dev.agent_tests.models import (
    TestCase,
    TestRun,
    CoverageGap,
    TestFactory,
)

__version__ = VERSION

# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

# -*- coding: utf-8 -*-

"""Main TestsAgent class for test suite improvement."""

# from src.core.base.BaseAgent import BaseAgent, create_main_function


class TestsAgent(BaseAgent):
    """Updates code file test suites using AI assistance.

    Invariants:
    - self.file_path must point to a test file (usually starting with 'test_').
    - The agent attempts to locate the corresponding source file to provide context.
    """

    __test__ = False

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

        # Test management
        self._tests: list[TestCase] = []
        self._test_runs: list[TestRun] = []
        self._coverage_gaps: list[CoverageGap] = []
        self._factories: dict[str, TestFactory] = {}

        # Configuration
        self._flakiness_threshold: float = 0.1  # 10% failure rate=flaky
        self._parallel_enabled: bool = False
        self._max_parallel: int = 4

    # ========== Test Management ==========

    def add_test(
        self,
        name: str,
        file_path: str,
        line_number: int,
        priority: TestPriority = TestPriority.MEDIUM,
        tags: list[str] | None = None,
        dependencies: list[str] | None = None,
    ) -> TestCase:
        """Add a new test case."""
        test_id = hashlib.md5(f"{name}:{file_path}".encode()).hexdigest()[:8]
        test = TestCase(
            id=test_id,
            name=name,
            file_path=file_path,
            line_number=line_number,
            priority=priority,
            tags=tags or [],
            dependencies=dependencies or [],
        )
        self._tests.append(test)
        return test

    def get_tests(self) -> list[TestCase]:
        """Get all tests."""
        return self._tests

    def get_test_by_id(self, test_id: str) -> TestCase | None:
        """Get test by ID."""
        return next((t for t in self._tests if t.id == test_id), None)

    def get_test_by_name(self, name: str) -> TestCase | None:
        """Get test by name."""
        return next((t for t in self._tests if t.name == name), None)

    def get_tests_by_priority(self, priority: TestPriority) -> list[TestCase]:
        """Get tests filtered by priority."""
        return [t for t in self._tests if t.priority == priority]

    def get_tests_by_tag(self, tag: str) -> list[TestCase]:
        """Get tests with a specific tag."""
        return [t for t in self._tests if tag in t.tags]

    # ========== Test Prioritization ==========

    def prioritize_tests(self) -> list[TestCase]:
        """Return tests sorted by priority (highest first)."""
        return sorted(
            self._tests, key=lambda t: (t.priority.value, t.failure_count), reverse=True
        )

    def calculate_priority_score(self, test: TestCase) -> float:
        """Calculate a priority score for a test."""
        score: float = test.priority.value * 20

        # Boost score for tests that fail often
        if test.run_count > 0:
            failure_rate = test.failure_count / test.run_count
            score += failure_rate * 30

        # Boost score for faster tests (they're cheaper to run)
        if test.duration_ms > 0 and test.duration_ms < 100:
            score += 10

        # Reduce score for flaky tests
        score -= test.flakiness_score * 20

        return max(0, min(100, score))

    def get_critical_tests(self) -> list[TestCase]:
        """Get tests marked as critical."""
        return [t for t in self._tests if t.priority == TestPriority.CRITICAL]

    # ========== Flakiness Detection ==========

    def calculate_flakiness(self, test: TestCase) -> float:
        """Calculate flakiness score for a test."""
        if test.run_count < 5:
            return 0.0  # Not enough data

        failure_rate = test.failure_count / test.run_count
        return failure_rate

    def detect_flaky_tests(self) -> list[TestCase]:
        """Detect tests that are flaky."""
        flaky: list[TestCase] = []
        for test in self._tests:
            score = self.calculate_flakiness(test)
            if score > self._flakiness_threshold:
                test.flakiness_score = score
                test.status = TestStatus.FLAKY
                flaky.append(test)
        return flaky

    def set_flakiness_threshold(self, threshold: float) -> None:
        """Set the flakiness threshold."""
        self._flakiness_threshold = max(0.0, min(1.0, threshold))

    def quarantine_flaky_test(self, test_id: str) -> bool:
        """Quarantine a flaky test by marking it for skip."""
        test = self.get_test_by_id(test_id)
        if test:
            test.priority = TestPriority.SKIP
            test.tags.append("quarantined")
            return True
        return False

    # ========== Coverage Gap Analysis ==========

    def add_coverage_gap(
        self,
        file_path: str,
        line_start: int,
        line_end: int,
        coverage_type: CoverageType = CoverageType.LINE,
        suggestion: str = "",
    ) -> CoverageGap:
        """Add a coverage gap."""
        gap = CoverageGap(
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            coverage_type=coverage_type,
            suggestion=suggestion,
        )
        self._coverage_gaps.append(gap)
        return gap

    def get_coverage_gaps(self) -> list[CoverageGap]:
        """Get all coverage gaps."""
        return self._coverage_gaps

    def get_coverage_gaps_by_file(self, file_path: str) -> list[CoverageGap]:
        """Get coverage gaps for a specific file."""
        return [g for g in self._coverage_gaps if g.file_path == file_path]

    def suggest_tests_for_gap(self, gap: CoverageGap) -> str:
        """Generate test suggestion for a coverage gap."""
        file_name = gap.file_path.replace("/", "_").replace(".py", "")
        suggestion_body = (
            gap.suggestion
            or f"assert True  # Placeholder for {gap.coverage_type.value} coverage"
        )
        return (
            f"# Suggested test for {gap.file_path} "
            f"lines {gap.line_start}-{gap.line_end}\n"
            f"def test_{file_name}_line{gap.line_start}():\n"
            f"    # Auto-generated path for {gap.coverage_type.value} coverage\n"
            f"    {suggestion_body}\n"
        )

    # ========== Test Data Factories ==========

    def add_factory(
        self,
        name: str,
        return_type: str,
        parameters: dict[str, str] | None = None,
        generator: str = "",
    ) -> TestFactory:
        """Add a test data factory."""
        factory = TestFactory(
            name=name,
            return_type=return_type,
            parameters=parameters or {},
            generator=generator,
        )
        self._factories[name] = factory
        return factory

    def get_factory(self, name: str) -> TestFactory | None:
        """Get a factory by name."""
        return self._factories.get(name)

    def get_factories(self) -> dict[str, TestFactory]:
        """Get all factories."""
        return self._factories

    def generate_factory_code(self, factory: TestFactory) -> str:
        """Generate code for a factory function."""
        params = ", ".join(f"{k}: {v}" for k, v in factory.parameters.items())
        return (
            f"def {factory.name}({params}) -> {factory.return_type}:\n"
            f'    """Factory for creating {factory.return_type} instances."""\n'
            f"    {factory.generator or 'pass'}\n"
        )

    # ========== Test Execution Recording ==========

    def record_test_run(
        self, test_results: dict[str, TestStatus], duration_ms: float = 0.0
    ) -> TestRun:
        """Record a test execution run."""
        run_id = hashlib.md5(
            f"{datetime.now().isoformat()}:{len(test_results)}".encode()
        ).hexdigest()[:8]

        passed = sum(1 for s in test_results.values() if s == TestStatus.PASSED)
        failed = sum(1 for s in test_results.values() if s == TestStatus.FAILED)
        skipped = sum(1 for s in test_results.values() if s == TestStatus.SKIPPED)
        errors = sum(1 for s in test_results.values() if s == TestStatus.ERROR)

        run = TestRun(
            id=run_id,
            timestamp=datetime.now().isoformat(),
            total_tests=len(test_results),
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            duration_ms=duration_ms,
            test_results=test_results,
        )
        self._test_runs.append(run)

        # Update individual test statistics
        for test_name, status in test_results.items():
            test = self.get_test_by_name(test_name)
            if test:
                test.run_count += 1
                test.last_run = run.timestamp
                if status == TestStatus.FAILED:
                    test.failure_count += 1

        return run

    def get_test_runs(self) -> list[TestRun]:
        """Get all test runs."""
        return self._test_runs

    def get_latest_run(self) -> TestRun | None:
        """Get the most recent test run."""
        return self._test_runs[-1] if self._test_runs else None

    # ========== Parallel Execution ==========

    def enable_parallel(self, max_workers: int = 4) -> None:
        """Enable parallel test execution."""
        self._parallel_enabled = True
        self._max_parallel = max_workers

    def disable_parallel(self) -> None:
        """Disable parallel test execution."""
        self._parallel_enabled = False

    def is_parallel_enabled(self) -> bool:
        """Check if parallel execution is enabled."""
        return self._parallel_enabled

    def get_parallel_groups(self) -> list[list[TestCase]]:
        """Group tests for parallel execution."""
        if not self._parallel_enabled:
            return [self._tests]

        # Group by dependencies - tests with same deps can't run in parallel
        groups: list[list[TestCase]] = []
        assigned: set[str] = set()

        for test in self._tests:
            if test.id in assigned:
                continue

            group = [test]
            assigned.add(test.id)

            # Find other tests that can run with this one
            for other in self._tests:
                if other.id in assigned:
                    continue
                # No dependency conflicts
                if not any(d in test.dependencies for d in other.dependencies):
                    if len(group) < self._max_parallel:
                        group.append(other)
                        assigned.add(other.id)

            groups.append(group)

        return groups

    # ========== Documentation Generation ==========

    def generate_test_documentation(self) -> str:
        """Generate documentation for all tests."""
        docs = ["# Test Documentation\n"]
        # Summary
        docs.append("## Summary\n")
        docs.append(f"- Total Tests: {len(self._tests)}")
        docs.append(
            f"- Critical: {len(self.get_tests_by_priority(TestPriority.CRITICAL))}"
        )
        docs.append(f"- Flaky: {len(self.detect_flaky_tests())}")
        docs.append(f"- Coverage Gaps: {len(self._coverage_gaps)}\n")
        # Tests by priority
        docs.append("## Tests by Priority\n")
        for priority in TestPriority:
            tests = self.get_tests_by_priority(priority)
            if tests:
                docs.append(f"### {priority.name}\n")
                for test in tests:
                    status_icon = "✓" if test.status == TestStatus.PASSED else "✗"
                    docs.append(
                        f"- [{status_icon}] `{test.name}` (line {test.line_number})"
                    )
                docs.append("")
        return "\n".join(docs)

    def export_tests(self, format: str = "json") -> str:
        """Export tests to various formats."""
        if format == "json":
            data: list[dict[str, Any]] = [
                {
                    "id": t.id,
                    "name": t.name,
                    "file": t.file_path,
                    "line": t.line_number,
                    "priority": t.priority.name,
                    "status": t.status.value,
                    "flakiness": t.flakiness_score,
                    "tags": t.tags,
                }
                for t in self._tests
            ]
            return json.dumps(data, indent=2)
        return ""

    # ========== Statistics ==========
    def calculate_statistics(self) -> dict[str, Any]:
        """Calculate test statistics."""
        total = len(self._tests)
        if total == 0:
            return {"total_tests": 0}
        by_status = {}
        for status in TestStatus:
            count = len([t for t in self._tests if t.status == status])
            by_status[status.name] = count
        by_priority = {}
        for priority in TestPriority:
            count = len([t for t in self._tests if t.priority == priority])
            by_priority[priority.name] = count
        avg_duration = (
            sum(t.duration_ms for t in self._tests) / total if total > 0 else 0
        )
        flaky_count = len(
            [t for t in self._tests if t.flakiness_score > self._flakiness_threshold]
        )
        return {
            "total_tests": total,
            "by_status": by_status,
            "by_priority": by_priority,
            "average_duration_ms": avg_duration,
            "flaky_tests": flaky_count,
            "coverage_gaps": len(self._coverage_gaps),
            "factories": len(self._factories),
            "test_runs": len(self._test_runs),
        }

    # ========== Original Methods ==========
    def _get_default_content(self) -> str:
        """Return default content for new test files."""
        return "# Tests\n\nimport pytest\n\n# Add tests here\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return (
            "# AI Improvement Unavailable\n# GitHub CLI not found. Install from "
            "https://cli.github.com/\n\n# Original test code preserved below:\n\n"
        )

    def _find_source_file(self) -> Path | None:
        """Locate source file for test file (test_foo.py -> foo.py)."""
        if not self.file_path.name.startswith("test_"):
            return None
        source_name = self.file_path.name[5:]  # Remove test_ prefix
        # Try to find source file in common locations
        # 1. Same directory
        source_path = self.file_path.parent / source_name
        if source_path.exists():
            return source_path
        # 2. Parent directory (if tests are in tests/)
        if self.file_path.parent.name == "tests":
            source_path = self.file_path.parent.parent / source_name
            if source_path.exists():
                return source_path
        # 3. scripts / agent directory (specific to this project structure)
        agent_dir = self.file_path.parent.parent / "scripts" / "agent"
        source_path = agent_dir / source_name
        if source_path.exists():
            return source_path
        return None

    def _validate_syntax(self, content: str) -> bool:
        """Validate Python syntax using ast."""
        try:
            ast.parse(content)
            return True
        except SyntaxError as e:
            logging.error(f"Syntax error in generated tests: {e}")
            return False

    def _validate_test_structure(self, content: str) -> bool:
        """Validate pytest / unittest-specific patterns."""
        try:
            tree = ast.parse(content)
            issues: list[str] = []
            # Check 1: All test functions follow naming convention
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if (
                        not node.name.startswith("test_")
                        and "test" in node.name.lower()
                    ):
                        # Just a warning, might be a helper
                        pass
            # Check 2: Tests contain assertions
            test_funcs = [
                n
                for n in ast.walk(tree)
                if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
            ]
            for func in test_funcs:
                has_assert = any(isinstance(n, ast.Assert) for n in ast.walk(func))
                # Simple check for pytest.raises context manager
                has_raises = False
                for node in ast.walk(func):
                    if isinstance(node, ast.With):
                        for item in node.items:
                            if isinstance(item.context_expr, ast.Call):
                                if isinstance(item.context_expr.func, ast.Attribute):
                                    if item.context_expr.func.attr == "raises":
                                        has_raises = True
                if not (has_assert or has_raises):
                    issues.append(f"Test '{func.name}' lacks assertions")
            if issues:
                logging.warning(f"Test structure issues: {', '.join(issues)}")
                # We don't fail validation for this yet, just warn
            return True
        except Exception as e:
            logging.warning(f"Failed to validate test structure: {e}")
            return True

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the test suites.

        When Copilot CLI is unavailable, BaseAgent keeps the existing content
        unchanged (avoids injecting duplicated placeholder markdown blocks).
        """
        logging.info(f"Improving tests for {self.file_path}")
        # Enhance prompt with source code context if available
        source_path = self._find_source_file()
        enhanced_prompt = prompt
        if source_path and source_path.exists():
            logging.debug(f"Using source file context: {source_path}")
            try:
                source_content = source_path.read_text(encoding="utf-8")
                # Truncate source content if it's too large to avoid context window issues
                # Assuming ~4 chars per token, 8000 tokens ~ 32000 chars.
                # Leave room for prompt and response.
                max_source_chars = 20000
                if len(source_content) > max_source_chars:
                    source_content = (
                        source_content[:max_source_chars] + "\n# ... (truncated)"
                    )
                enhanced_prompt = (
                    f"{prompt}\n\n"
                    f"# Source Code being tested ({source_path.name}):\n"
                    f"```python\n{source_content}\n```\n\n"
                    "Ensure tests cover the public API and edge cases of the source code."
                )
            except Exception as e:
                logging.warning(f"Failed to read source file context: {e}")
        new_content = super().improve_content(enhanced_prompt)
        # Validate syntax

        if not self._validate_syntax(new_content):
            logging.error("Generated tests failed syntax validation. Reverting.")
            self.current_content = self.previous_content

            return self.previous_content
        logging.debug("Syntax validation passed")
        # Validate structure
        self._validate_test_structure(new_content)

        return new_content

    def update_file(self) -> bool:
        """Write the improved content back to the file (no markdown fixing for test files)."""
        self.file_path.write_text(self.current_content, encoding="utf-8")

        return True


# create_main_function is not available in the current refactored structure
# def main() would need to be implemented separately if needed for CLI use
# main = create_main_function(


#    TestsAgent,
#    'Tests Agent: Updates code file test suites',
#    'Path to the tests file (e.g., test_file.py)'
# )


if __name__ == "__main__":
    # CLI interface would be implemented here if needed
    pass
