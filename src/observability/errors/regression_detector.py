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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

import re

from src.core.base.lifecycle.version import VERSION

from .error_entry import ErrorEntry
from .regression_info import RegressionInfo

__version__ = VERSION


class RegressionDetector:
    """Detects error regressions.

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
