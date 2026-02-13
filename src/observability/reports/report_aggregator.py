#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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


"""
Report Aggregator - Combine and summarize CodeIssue lists into an AggregatedReport

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate ReportAggregator, add per-file issue lists, then call aggregate() to get an AggregatedReport.
- Example:
    from report_aggregator import ReportAggregator
    agg = ReportAggregator()
    agg.add_source("module_a.py", issues_a)
    agg.add_source("module_b.py", issues_b)
    report = agg.aggregate()
    agg.clear()

WHAT IT DOES:
- Collects CodeIssue lists keyed by source file and merges them into a single AggregatedReport.
- Produces simple summary counts: total issues, total files, breakdowns by severity and by category.
- Preserves the original issue objects in combined_issues and exposes the list of source file paths.

WHAT IT SHOULD DO BETTER:
- Deduplicate or intelligently merge identical issues reported from multiple sources and optionally preserve provenance per issue.
- Support incremental/streaming aggregation and memory-efficient handling for very large issue sets.
- Add input validation, thread-safety (or async-safe) APIs, richer summary metrics (e.g., per-file counts, temporal trends), configurable severity/category mapping, and better logging and error handling.
- Provide unit tests for edge cases (empty input, non-CodeIssue items), type narrowing, and clearer serialization for AggregatedReport output formats (JSON/CSV).

FILE CONTENT SUMMARY:
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

import logging

from src.core.base.lifecycle.version import VERSION

from .aggregated_report import AggregatedReport
from .code_issue import CodeIssue

__version__ = VERSION


class ReportAggregator:
    """Aggregator for combining reports from multiple sources.
    Combines and summarizes reports across files.
    Example:
        aggregator=ReportAggregator()
        aggregator.add_source("file1.py", issues1)
        aggregator.add_source("file2.py", issues2)
        combined=aggregator.aggregate()
    """

    def __init__(self) -> None:
        """Initialize aggregator."""

        self.sources: dict[str, list[CodeIssue]] = {}
        logging.debug("ReportAggregator initialized")

    def add_source(self, file_path: str, issues: list[CodeIssue]) -> None:
        """Add a source to aggregate.
        Args:
            file_path: Source file.
            issues: Issues from file.
        """

        self.sources[file_path] = issues

    def aggregate(self) -> AggregatedReport:
        """Aggregate all sources.
        Returns:
            Aggregated report.
        """

        all_issues: list[CodeIssue] = []
        for issues in self.sources.values():
            all_issues.extend(issues)
        # Calculate summary
        by_severity: dict[str, int] = {}
        by_category: dict[str, int] = {}
        for issue in all_issues:
            sev = issue.severity.name
            cat = issue.category.name
            by_severity[sev] = by_severity.get(sev, 0) + 1
            by_category[cat] = by_category.get(cat, 0) + 1
        return AggregatedReport(
            sources=list(self.sources.keys()),
            combined_issues=all_issues,
            summary={
                "total_issues": len(all_issues),
                "total_files": len(self.sources),
                "by_severity": by_severity,
                "by_category": by_category,
            },
        )

    def clear(self) -> None:
        """Clear all sources."""

        self.sources.clear()
"""

from __future__ import annotations

import logging

from src.core.base.lifecycle.version import VERSION

from .aggregated_report import AggregatedReport
from .code_issue import CodeIssue

__version__ = VERSION


class ReportAggregator:
    """Aggregator for combining reports from multiple sources.
    Combines and summarizes reports across files.
    Example:
        aggregator=ReportAggregator()
        aggregator.add_source("file1.py", issues1)
        aggregator.add_source("file2.py", issues2)
        combined=aggregator.aggregate()
    """

    def __init__(self) -> None:
        """Initialize aggregator."""

        self.sources: dict[str, list[CodeIssue]] = {}
        logging.debug("ReportAggregator initialized")

    def add_source(self, file_path: str, issues: list[CodeIssue]) -> None:
        """Add a source to aggregate.
        Args:
            file_path: Source file.
            issues: Issues from file.
        """

        self.sources[file_path] = issues

    def aggregate(self) -> AggregatedReport:
        """Aggregate all sources.
        Returns:
            Aggregated report.
        """

        all_issues: list[CodeIssue] = []
        for issues in self.sources.values():
            all_issues.extend(issues)
        # Calculate summary
        by_severity: dict[str, int] = {}
        by_category: dict[str, int] = {}
        for issue in all_issues:
            sev = issue.severity.name
            cat = issue.category.name
            by_severity[sev] = by_severity.get(sev, 0) + 1
            by_category[cat] = by_category.get(cat, 0) + 1
        return AggregatedReport(
            sources=list(self.sources.keys()),
            combined_issues=all_issues,
            summary={
                "total_issues": len(all_issues),
                "total_files": len(self.sources),
                "by_severity": by_severity,
                "by_category": by_category,
            },
        )

    def clear(self) -> None:
        """Clear all sources."""

        self.sources.clear()
