#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Regression Detector - Detecting reappeared fixed errors

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Import RegressionDetector from regression_detector and use:
- detector = RegressionDetector()
- detector.record_fix(error_entry, commit_hash)
- detector.check_regression(error_entry, current_commit) -> RegressionInfo | None
- detector.get_regressions() and detector.get_regression_rate() for reporting

WHAT IT DOES:
Maintains a map of signatures for errors that were previously recorded as fixed and detects when the same signature reappears, producing RegressionInfo entries and counting repeated occurrences. Produces a simple regression rate as (detected regressions / recorded fixes) * 100.

WHAT IT SHOULD DO BETTER:
- Signature robustness: normalize more than digits (whitespace, paths, stack traces, variable names) and consider fuzzy or token-based matching to reduce false positives/negatives.
- Persistence & provenance: persist fixed_errors and regressions (database or file) and record timestamps and author metadata for better auditing.
- Concurrency & scale: make thread/process-safe, support bulk updates, and limit memory growth for long-running agents.
- Reporting & thresholds: support configurable thresholds, time-windows, and deduplication rules; surface context (stack trace, snippet) with regression reports.
- Testing & typing: add unit tests for edge cases and stronger type hints / validation for ErrorEntry contents.
"""

try:
    import re
except ImportError:
    import re


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .error_entry import ErrorEntry
except ImportError:
    from .error_entry import ErrorEntry

try:
    from .regression_info import RegressionInfo
except ImportError:
    from .regression_info import RegressionInfo


__version__ = VERSION


class RegressionDetector:
    """
    Detects error regressions.
    Identifies errors that were previously fixed but have reappeared
    in the codebase.

    Attributes:
        fixed_errors: Map of fixed error signatures to commit info.
    """

    def __init__(self) -> None:
        """Initialize the regression detector."""
        self.fixed_errors: dict[str, str] = {}  # signature -> fix_commit
        self.regressions: list[RegressionInfo] = []


    def record_fix(self, error: ErrorEntry, commit_hash: str) -> None:
        """Record that an error was fixed.
        Args:
            error: The fixed error.
            commit_hash: The commit that fixed the error.
        """
        signature = self._get_error_signature(error)
        self.fixed_errors[signature] = commit_hash


    def check_regression(self, error: ErrorEntry, current_commit: str = "") -> RegressionInfo | None:
        """Check if an error is a regression.
        Args:
            error: The error to check.
            current_commit: Current commit hash.

        Returns:
            RegressionInfo if this is a regression, None otherwise.
        """
        signature = self._get_error_signature(error)
        if signature in self.fixed_errors:
            regression = RegressionInfo(
                error_id=error.id,
                original_fix_commit=self.fixed_errors[signature],
                regression_commit=current_commit,
            )
            # Check if already tracked
            for r in self.regressions:
                if r.error_id == error.id:
                    r.occurrences += 1
                    return r
            self.regressions.append(regression)
            return regression
        return None


    def _get_error_signature(self, error: ErrorEntry) -> str:
        """Generate a signature for an error."""
        normalized = re.sub(r"\d+", "N", error.message)
        return f"{error.file_path}:{normalized}"


    def get_regressions(self) -> list[RegressionInfo]:
        """Get all detected regressions."""
        return self.regressions


    def get_regression_rate(self) -> float:
        """Calculate the regression rate."""
        if not self.fixed_errors:
            return 0.0
        return len(self.regressions) / len(self.fixed_errors) * 100
