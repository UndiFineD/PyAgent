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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from generate_agent_reports.py"""



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
