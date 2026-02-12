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


"""
ChangelogSearcher - Search changelog content

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate and call search(query, content) to get a list of SearchResult objects ordered by relevance.
- Example:
    searcher = ChangelogSearcher()
    results = searcher.search("bug fix", changelog_text)
    for r in results:
        print(r.version, r.line_number, r.match_score, r.context)

WHAT IT DOES:
- Searches changelog text for a query and returns SearchResult entries with version, line number, context, and a computed match_score.
- Prefers Rust-accelerated routines (extract_versions_rust, search_content_scored_rust) when available for version extraction and scored searching; falls back to a pure-Python implementation when Rust modules are unavailable or raise errors.
- Python fallback extracts semantic version headings matching patterns like "## [1.2.3]" or date-style "## 2026.02.12", tracks the current version per line, finds case-insensitive matches, and scores matches via _calculate_score (exact match=1.0, word-boundary=0.8, substring=0.5).

WHAT IT SHOULD DO BETTER:
- More robust version header parsing (support more semantic version formats, pre-releases, and arbitrary header levels) and extraction of multi-line changelog entries rather than single-line contexts.
- Use a configurable, explainable scoring model (TF-IDF, fuzzy matching, position/recency weighting) and expose scoring parameters to callers.
- Return richer context windows (surrounding lines, structured entry blocks) and support streaming/large-file processing to avoid loading very large changelogs into memory.
- Improve error handling and logging for Rust fallback, add unit tests for both Rust and Python paths, and document expected SearchResult fields and types in the module-level docstring.

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


"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

import re

from src.core.base.common.types.search_result import SearchResult
from src.core.base.lifecycle.version import VERSION

# Rust acceleration imports
try:
    from rust_core import extract_versions_rust, search_content_scored_rust

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

__version__ = VERSION


class ChangelogSearcher:
    """Searches changelog content across project history.

    Provides search functionality for finding specific entries
    in changelog history.

    Example:
        >>> searcher=ChangelogSearcher()
        >>> results=searcher.search("bug fix", changelog_content)
    """

    def search(self, query: str, content: str) -> list[SearchResult]:
        """Search for query in changelog content.

        Args:
            query: Search query string.
            content: Changelog content to search.

        Returns:
            List of search results.
        """
        # Rust-accelerated search
        if _RUST_AVAILABLE:
            try:
                # Extract versions first
                versions = extract_versions_rust(content)
                version_map = {}
                current_ver = "Unknown"
                lines = content.split("\n")
                for line_num, ver in versions:
                    version_map[line_num] = ver

                # Build line->version mapping
                line_versions = {}
                for i in range(1, len(lines) + 1):
                    if i in version_map:
                        current_ver = version_map[i]
                    line_versions[i] = current_ver

                # Search with scoring
                matches = search_content_scored_rust(query, content)
                results = [
                    SearchResult(
                        version=line_versions.get(line_num, "Unknown"),
                        line_number=line_num,
                        context=ctx,
                        match_score=score,
                    )
                    for line_num, score, ctx in matches
                ]
                return results
            except (AttributeError, TypeError, RuntimeError, OSError):
                pass  # Fall back to Python

        # Python fallback
        results = []
        lines = content.split("\n")
        current_version = "Unknown"
        for i, line in enumerate(lines, 1):
            # Track current version
            version_match = re.match(r"##\s*\[?(\d+\.\d+\.\d+|\d{4}\.\d{2}\.\d{2})\]?", line)
            if version_match:
                current_version = version_match.group(1)
            # Search for query
            if query.lower() in line.lower():
                results.append(
                    SearchResult(
                        version=current_version,
                        line_number=i,
                        context=line.strip(),
                        match_score=self._calculate_score(query, line),
                    )
                )
        return sorted(results, key=lambda r: r.match_score, reverse=True)

    def _calculate_score(self, query: str, text: str) -> float:
        """Calculate relevance score for a match.

        Args:
            query: Search query.
            text: Text containing the match.

        Returns:
            Score between 0 and 1.
        """
        query_lower = query.lower()
        text_lower = text.lower()
        # Exact match gets highest score
        if query_lower == text_lower:
            return 1.0
        # Word boundary match
        if re.search(rf"\b{re.escape(query_lower)}\b", text_lower):
            return 0.8
        # Substring match
        return 0.5
"""

from __future__ import annotations

import re

from src.core.base.common.types.search_result import SearchResult
from src.core.base.lifecycle.version import VERSION

# Rust acceleration imports
try:
    from rust_core import extract_versions_rust, search_content_scored_rust

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

__version__ = VERSION


class ChangelogSearcher:
    """Searches changelog content across project history.

    Provides search functionality for finding specific entries
    in changelog history.

    Example:
        >>> searcher=ChangelogSearcher()
        >>> results=searcher.search("bug fix", changelog_content)
    """

    def search(self, query: str, content: str) -> list[SearchResult]:
        """Search for query in changelog content.

        Args:
            query: Search query string.
            content: Changelog content to search.

        Returns:
            List of search results.
        """
        # Rust-accelerated search
        if _RUST_AVAILABLE:
            try:
                # Extract versions first
                versions = extract_versions_rust(content)
                version_map = {}
                current_ver = "Unknown"
                lines = content.split("\n")
                for line_num, ver in versions:
                    version_map[line_num] = ver

                # Build line->version mapping
                line_versions = {}
                for i in range(1, len(lines) + 1):
                    if i in version_map:
                        current_ver = version_map[i]
                    line_versions[i] = current_ver

                # Search with scoring
                matches = search_content_scored_rust(query, content)
                results = [
                    SearchResult(
                        version=line_versions.get(line_num, "Unknown"),
                        line_number=line_num,
                        context=ctx,
                        match_score=score,
                    )
                    for line_num, score, ctx in matches
                ]
                return results
            except (AttributeError, TypeError, RuntimeError, OSError):
                pass  # Fall back to Python

        # Python fallback
        results = []
        lines = content.split("\n")
        current_version = "Unknown"
        for i, line in enumerate(lines, 1):
            # Track current version
            version_match = re.match(r"##\s*\[?(\d+\.\d+\.\d+|\d{4}\.\d{2}\.\d{2})\]?", line)
            if version_match:
                current_version = version_match.group(1)
            # Search for query
            if query.lower() in line.lower():
                results.append(
                    SearchResult(
                        version=current_version,
                        line_number=i,
                        context=line.strip(),
                        match_score=self._calculate_score(query, line),
                    )
                )
        return sorted(results, key=lambda r: r.match_score, reverse=True)

    def _calculate_score(self, query: str, text: str) -> float:
        """Calculate relevance score for a match.

        Args:
            query: Search query.
            text: Text containing the match.

        Returns:
            Score between 0 and 1.
        """
        query_lower = query.lower()
        text_lower = text.lower()
        # Exact match gets highest score
        if query_lower == text_lower:
            return 1.0
        # Word boundary match
        if re.search(rf"\b{re.escape(query_lower)}\b", text_lower):
            return 0.8
        # Substring match
        return 0.5
