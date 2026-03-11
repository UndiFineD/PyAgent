#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/observability/reports/report_filter.description.md

# Description: src/observability/reports/report_filter.py

Module overview:
- `ReportFilter` filters `CodeIssue` objects based on a `FilterCriteria` (severity, categories).
- Exposes `matches` and `filter_issues` methods.

Behavioral notes:
- Simple predicate-based filtering; relies on `FilterCriteria` and `CodeIssue` definitions.
## Source: src-old/observability/reports/report_filter.improvements.md

# Improvements: src/observability/reports/report_filter.py

Potential improvements:
- Add unit tests for filtering logic across combinations of criteria.
- Support more complex boolean filters (AND/OR), and negation for categories.
- Allow filtering by filename, line ranges, and function names.
- Support configurable default `FilterCriteria` via dependency injection.

LLM_CONTEXT_END
"""

from __future__ import annotations

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


from src.core.base.lifecycle.version import VERSION

from .code_issue import CodeIssue
from .filter_criteria import FilterCriteria

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
        if self.criteria.min_severity and issue.severity.value < self.criteria.min_severity.value:
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
