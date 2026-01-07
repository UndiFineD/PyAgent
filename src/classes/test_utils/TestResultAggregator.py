#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from .TestResult import TestResult
from .TestStatus import TestStatus

from typing import Any, Dict, List, Optional, Union

class TestResultAggregator:
    __test__ = False
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
