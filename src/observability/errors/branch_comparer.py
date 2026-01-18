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
from src.core.base.version import VERSION
from .BranchComparison import BranchComparison
from typing import Dict, List, Set

__version__ = VERSION

class BranchComparer:
    """Compares errors across git branches.

    Identifies errors that exist only in specific branches
    or are common across branches.

    Attributes:
        branch_errors: Map of branch names to error sets.
    """

    def __init__(self) -> None:
        """Initialize the branch comparer."""
        self.branch_errors: dict[str, set[str]] = {}

    def set_branch_errors(
        self, branch: str, error_ids: list[str]
    ) -> None:
        """Set errors for a branch.

        Args:
            branch: Branch name.
            error_ids: List of error IDs in the branch.
        """
        self.branch_errors[branch] = set(error_ids)

    def compare(self, branch_a: str, branch_b: str) -> BranchComparison:
        """Compare errors between two branches.

        Args:
            branch_a: First branch name.
            branch_b: Second branch name.

        Returns:
            BranchComparison with differences.
        """
        errors_a = self.branch_errors.get(branch_a, set())
        errors_b = self.branch_errors.get(branch_b, set())

        return BranchComparison(
            branch_a=branch_a,
            branch_b=branch_b,
            errors_only_in_a=list(errors_a - errors_b),
            errors_only_in_b=list(errors_b - errors_a),
            common_errors=list(errors_a & errors_b)
        )

    def get_new_errors(
        self, base_branch: str, feature_branch: str
    ) -> list[str]:
        """Get errors introduced in feature branch.

        Args:
            base_branch: Base branch name (e.g., main).
            feature_branch: Feature branch name.

        Returns:
            List of error IDs only in feature branch.
        """
        comparison = self.compare(base_branch, feature_branch)
        return comparison.errors_only_in_b

    def get_fixed_errors(
        self, base_branch: str, feature_branch: str
    ) -> list[str]:
        """Get errors fixed in feature branch.

        Args:
            base_branch: Base branch name.
            feature_branch: Feature branch name.

        Returns:
            List of error IDs fixed in feature branch.
        """
        comparison = self.compare(base_branch, feature_branch)
        return comparison.errors_only_in_a