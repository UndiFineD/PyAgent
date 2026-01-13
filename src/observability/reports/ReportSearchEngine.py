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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .ReportSearchResult import ReportSearchResult
from .ReportType import ReportType
from typing import Dict, List, Tuple
import logging
import re

__version__ = VERSION

class ReportSearchEngine:
    """Search engine for reports.
    Enables full - text search across historical report data.
    Attributes:
        index: Search index mapping terms to locations.
    Example:
        engine=ReportSearchEngine()
        engine.index_report("file.py", ReportType.ERRORS, content)
        results=engine.search("syntax error")
    """

    def __init__(self) -> None:
        """Initialize search engine."""

        self.index: dict[str, list[tuple[str, ReportType, int]]] = {}
        self._reports: dict[str, str] = {}
        logging.debug("ReportSearchEngine initialized")

    def index_report(
        self,
        file_path: str,
        report_type: ReportType,
        content: str
    ) -> None:
        """Index a report for searching.
        Args:
            file_path: Report file path.
            report_type: Type of report.
            content: Report content.
        """

        key = f"{file_path}:{report_type.name}"
        self._reports[key] = content
        # Build index
        for line_num, line in enumerate(content.split("\n"), 1):
            words = re.findall(r'\w+', line.lower())
            for word in words:
                if word not in self.index:
                    self.index[word] = []
                self.index[word].append((file_path, report_type, line_num))

    def search(self, query: str, max_results: int = 20) -> list[ReportSearchResult]:
        """Search reports.
        Args:
            query: Search query.
            max_results: Maximum results to return.
        Returns:
            List of search results.
        """

        words = re.findall(r'\w+', query.lower())
        matches: dict[str, int] = {}
        for word in words:
            if word in self.index:
                for file_path, report_type, line_num in self.index[word]:
                    key = f"{file_path}:{report_type.name}:{line_num}"
                    matches[key] = matches.get(key, 0) + 1
        results: list[ReportSearchResult] = []
        for key, score in sorted(matches.items(), key=lambda x: -x[1])[:max_results]:
            parts = key.split(":")
            file_path = parts[0]
            report_type = ReportType[parts[1]]
            line_num = int(parts[2])
            # Get match context
            report_key = f"{file_path}:{report_type.name}"
            content = self._reports.get(report_key, "")
            lines = content.split("\n")
            match_text = lines[line_num - 1] if line_num <= len(lines) else ""
            results.append(ReportSearchResult(
                file_path=file_path,
                report_type=report_type,
                match_text=match_text,
                line_number=line_num,
                score=float(score)
            ))
        return results