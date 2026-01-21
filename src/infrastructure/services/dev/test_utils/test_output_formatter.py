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


"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from typing import Any

__version__ = VERSION


class TestOutputFormatter:
    """Formats test output and results for display."""

    __test__ = False

    def __init__(self) -> None:
        """Initialize formatter."""
        self.results: list[tuple[str, str, float]] = []

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

    def format_result(
        self, test_name: str, status: Any, duration_ms: float, error_message: str = ""
    ) -> str:
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
        status_str = status.value if hasattr(status, "value") else str(status)
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
        status_str = status.value if hasattr(status, "value") else str(status)
        self.results.append((test_name, status_str, duration_ms))

    def get_summary(self) -> dict[str, int]:
        """Get a summary of all results as a dict.

        Returns:
            Summary dict with counts.
        """
        passed = sum(1 for _, status, _ in self.results if "pass" in status.lower())
        failed = sum(1 for _, status, _ in self.results if "fail" in status.lower())
        total = len(self.results)
        return {"passed": passed, "failed": failed, "total": total}
