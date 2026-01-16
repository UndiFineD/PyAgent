#!/usr/bin/env python3
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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from .TestResult import TestResult
from .TestStatus import TestStatus
from typing import Any

__version__ = VERSION


class TestResultAggregator:
    """Aggregates test results for reporting.

    Example:
        agg=TestResultAggregator()
        agg.add_result(TestResult(name="test1", status=TestStatus.PASSED))
        report=agg.get_report()
    """

    __test__ = False

    def __init__(self) -> None:
        """Initialize result aggregator."""
        self._results: list[TestResult] = []

    def add_result(
        self,
        result: TestResult | str,
        test_name: str | None = None,
        status: str | None = None,
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
                status=TestStatus[status.upper()]
                if hasattr(TestStatus, status.upper())
                else TestStatus.PASSED,
                duration_ms=0.0,
            )
            self._results.append(test_result)
        else:
            raise TypeError("Invalid arguments to add_result")

    def get_results(self) -> list[TestResult]:
        """Get all results."""
        return list(self._results)

    def get_report(self) -> dict[str, Any]:
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

    def get_summary(self) -> dict[str, Any]:
        """Compatibility alias used by some tests."""
        report = self.get_report()
        return {
            "total": report.get("total", 0),
            "passed": report.get("passed", 0),
            "failed": report.get("failed", 0),
            "skipped": report.get("skipped", 0),
            "errors": report.get("errors", 0),
        }

    def get_by_suite(self) -> dict[str, dict[str, int]]:
        """Group results by suite prefix ("suite/test")."""
        by_suite: dict[str, dict[str, int]] = {}
        for r in self._results:
            suite = "unknown"
            if "/" in r.test_name:
                suite = r.test_name.split("/", 1)[0]
            by_suite.setdefault(
                suite, {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0}
            )
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

    def get_failures(self) -> list[TestResult]:
        """Get failed tests."""
        return [r for r in self._results if r.status == TestStatus.FAILED]

    def clear(self) -> None:
        """Clear all results."""
        self._results.clear()
