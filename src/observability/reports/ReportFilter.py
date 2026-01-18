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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from .CodeIssue import CodeIssue
from .FilterCriteria import FilterCriteria

__version__ = VERSION


class ReportFilter:
    """Filters reports based on criteria.
    Attributes:
        criteria: Filter criteria to apply.
    """

    def __init__(self, criteria: FilterCriteria | None = None) -> None:
        """Initialize filter.
        Args:
            criteria: Filter criteria. Uses defaults if not provided.
        """

        self.criteria = criteria or FilterCriteria()

    def matches(self, issue: CodeIssue) -> bool:
        """Check if issue matches filter criteria.
        Args:
            issue: Code issue to check.
        Returns:
            True if issue matches all criteria.
        """

        # Check severity
        if (
            self.criteria.min_severity
            and issue.severity.value < self.criteria.min_severity.value
        ):
            return False
        # Check category
        if self.criteria.categories and issue.category not in self.criteria.categories:
            return False
        return True

    def filter_issues(self, issues: list[CodeIssue]) -> list[CodeIssue]:
        """Filter list of issues.
        Args:
            issues: List of issues to filter.
        Returns:
            Filtered list of issues.
        """

        return [i for i in issues if self.matches(i)]
