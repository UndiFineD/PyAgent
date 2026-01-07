#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from .AggregatedReport import AggregatedReport
from .CodeIssue import CodeIssue

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, cast
import ast
import hashlib
import json
import logging
import re
import sys
import time

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

        self.sources: Dict[str, List[CodeIssue]] = {}
        logging.debug("ReportAggregator initialized")

    def add_source(self, file_path: str, issues: List[CodeIssue]) -> None:
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

        all_issues: List[CodeIssue] = []
        for issues in self.sources.values():
            all_issues.extend(issues)
        # Calculate summary
        by_severity: Dict[str, int] = {}
        by_category: Dict[str, int] = {}
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
                "by_category": by_category
            }
        )

    def clear(self) -> None:
        """Clear all sources."""

        self.sources.clear()
