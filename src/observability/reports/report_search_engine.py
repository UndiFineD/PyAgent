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
Report Search Engine - Full-text indexing and query of report content

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate ReportSearchEngine(), call index_report(file_path, report_type, content) for each report, then call search(query, max_results=20) to retrieve ReportSearchResult objects with matched context and scores.

WHAT IT DOES:
Implements a lightweight in-memory full-text search engine for report contents with optional Rust acceleration: tokenizes and indexes report lines (mapping words to (file_path, ReportType, line_number)), stores original reports to provide context lines for matches, and returns ranked ReportSearchResult objects by match frequency.

WHAT IT SHOULD DO BETTER:
- Support phrase queries, boolean operators, and fuzzy matching for more accurate retrieval.
- Provide persistent on-disk indexing or memory-efficient structures for large histories.
- Expose incremental update/removal of indexed reports and better handling of ReportType name collisions.
- Surface provenance metadata (timestamps, report IDs) and highlight multiple surrounding context lines in results.
- Add unit tests for Rust-fallback edge cases and instrumentation for indexing/search performance.

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
import re

from src.core.base.lifecycle.version import VERSION

from .report_search_result import ReportSearchResult
from .report_type import ReportType

# Rust acceleration imports
try:
    from rust_core import tokenize_and_index_rust, tokenize_query_rust

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

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

    def index_report(self, file_path: str, report_type: ReportType, content: str) -> None:
        """Index a report for searching.
        Args:
            file_path: Report file path.
            report_type: Type of report.
            content: Report content.
        """

        key = f"{file_path}:{report_type.name}"
        self._reports[key] = content

        # Rust-accelerated indexing path
        if _RUST_AVAILABLE:
            try:
                rust_index = tokenize_and_index_rust(file_path, report_type.name, content)
                for word, locations in rust_index.items():
                    if word not in self.index:
                        self.index[word] = []
                    for fp, rt, ln in locations:
                        self.index[word].append((fp, ReportType[rt], ln))
                return
            except (AttributeError, TypeError, RuntimeError, OSError):
                pass  # Fall back to Python

        # Python fallback: Build index
        for line_num, line in enumerate(content.split("\n"), 1):
            words = re.findall(r"\w+", line.lower())
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

        # Rust-accelerated query tokenization
        if _RUST_AVAILABLE:
            try:
                words = tokenize_query_rust(query)
            except (AttributeError, TypeError, RuntimeError, OSError):
                words = re.findall(r"\w+", query.lower())
        else:
            words = re.findall(r"\w+", query.lower())

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
            results.append(
                ReportSearchResult(
                    file_path=file_path,
                    report_type=report_type,
                    match_text=match_text,
                    line_number=line_num,
                    score=float(score),
                )
            )
        return results
"""

from __future__ import annotations

import logging
import re

from src.core.base.lifecycle.version import VERSION

from .report_search_result import ReportSearchResult
from .report_type import ReportType

# Rust acceleration imports
try:
    from rust_core import tokenize_and_index_rust, tokenize_query_rust

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

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

    def index_report(self, file_path: str, report_type: ReportType, content: str) -> None:
        """Index a report for searching.
        Args:
            file_path: Report file path.
            report_type: Type of report.
            content: Report content.
        """

        key = f"{file_path}:{report_type.name}"
        self._reports[key] = content

        # Rust-accelerated indexing path
        if _RUST_AVAILABLE:
            try:
                rust_index = tokenize_and_index_rust(file_path, report_type.name, content)
                for word, locations in rust_index.items():
                    if word not in self.index:
                        self.index[word] = []
                    for fp, rt, ln in locations:
                        self.index[word].append((fp, ReportType[rt], ln))
                return
            except (AttributeError, TypeError, RuntimeError, OSError):
                pass  # Fall back to Python

        # Python fallback: Build index
        for line_num, line in enumerate(content.split("\n"), 1):
            words = re.findall(r"\w+", line.lower())
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

        # Rust-accelerated query tokenization
        if _RUST_AVAILABLE:
            try:
                words = tokenize_query_rust(query)
            except (AttributeError, TypeError, RuntimeError, OSError):
                words = re.findall(r"\w+", query.lower())
        else:
            words = re.findall(r"\w+", query.lower())

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
            results.append(
                ReportSearchResult(
                    file_path=file_path,
                    report_type=report_type,
                    match_text=match_text,
                    line_number=line_num,
                    score=float(score),
                )
            )
        return results
