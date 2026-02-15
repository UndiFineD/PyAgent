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
SearchCore - Search result parsing facade

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
from search_core import SearchCore
# parse provider responses into markdown-like result blocks
bing_blocks = SearchCore.parse_bing_results(bing_response)
google_blocks = SearchCore.parse_google_results(google_response)
ddg_blocks = SearchCore.parse_ddg_results(ddg_response)
# combine into a single formatted string
final = SearchCore.format_results_block(bing_blocks, provider="Bing")

WHAT IT DOES:
Provides a lightweight facade over the standard SearchCore implementation (src.core.base.common.search_core) that exposes static parsers for Bing, Google Custom Search, and DuckDuckGo results and a helper to combine parsed entries into a single provider-labeled block; attempts to use rust_core accelerated parsing when available and falls back to pure-Python parsing on import or runtime failures.

WHAT IT SHOULD DO BETTER:
- Surface structured metadata (source, timestamp, rank) instead of plain markdown strings to allow richer downstream processing.
- Log or surface why rust_core fallbacks occur for easier debugging and operational visibility.
- Add robust schema validation (pydantic/dataclasses) for incoming search payloads, unit tests for edge cases, and optionally async variants for large-volume parsing.

FILE CONTENT SUMMARY:
SearchCore logic for PyAgent.
(Facade for src.core.base.common.search_core)
"""

from __future__ import annotations

from typing import Any

from src.core.base.common.search_core import SearchCore as StandardSearchCore

try:
    import rust_core as rc

    HAS_RUST = True
except ImportError:
    rc = None
    HAS_RUST = False


class SearchCore(StandardSearchCore):
    """Facade for SearchCore logic, providing specialized parsing."""

    @staticmethod
    def parse_bing_results(data: dict[str, Any]) -> list[str]:
        """Parses Bing web search results into Markdown blocks."""
        if HAS_RUST and hasattr(rc, "parse_bing_results_rust"):
            try:
                return rc.parse_bing_results_rust(data)
            except (RuntimeError, ValueError, TypeError, AttributeError):
                pass

        results: list[str] = []
        for v in data.get("webPages", {}).get("value", []):
            name = v.get("name", "Untitled Result")
            url = v.get("url", "#")
            snippet = v.get("snippet", "No snippet available.")
            results.append(f"### {name}\nURL: {url}\n{snippet}\n")
        return results

    @staticmethod
    def parse_google_results(data: dict[str, Any]) -> list[str]:
        """Parses Google Custom Search results into Markdown blocks."""
        if HAS_RUST and hasattr(rc, "parse_google_results_rust"):
            try:
                return rc.parse_google_results_rust(data)
            except (RuntimeError, ValueError, TypeError, AttributeError):
                pass
        results: list[str] = []
        for item in data.get("items", []):
            title = item.get("title", "Untitled Result")
            link = item.get("link", "#")
            snippet = item.get("snippet", "No snippet available.")
            results.append(f"### {title}\nURL: {link}\n{snippet}\n")
        return results

    @staticmethod
    def parse_ddg_results(data: list[dict[str, Any]]) -> list[str]:
        """Parses DuckDuckGo results from ddg_search library format."""
        if HAS_RUST and hasattr(rc, "parse_ddg_results_rust"):
            try:
                return rc.parse_ddg_results_rust(data)
            except (RuntimeError, ValueError, TypeError, AttributeError):
                pass
        results: list[str] = []
        for r in data:
            title = r.get("title", "Untitled Result")
            href = r.get("href", "#")
            body = r.get("body", "No description available.")
            results.append(f"### {title}\nURL: {href}\n{body}\n")
        return results

    @staticmethod
    def format_results_block(results: list[str], provider: str) -> str:
        """Combines list of results into a single string with provider indicator."""
        if not results:
            return f"No {provider} results found."
        return "\n".join(results)
"""

from __future__ import annotations

from typing import Any

from src.core.base.common.search_core import SearchCore as StandardSearchCore

try:
    import rust_core as rc

    HAS_RUST = True
except ImportError:
    rc = None
    HAS_RUST = False


class SearchCore(StandardSearchCore):
    """Facade for SearchCore logic, providing specialized parsing."""

    @staticmethod
    def parse_bing_results(data: dict[str, Any]) -> list[str]:
        """Parses Bing web search results into Markdown blocks."""
        if HAS_RUST and hasattr(rc, "parse_bing_results_rust"):
            try:
                return rc.parse_bing_results_rust(data)
            except (RuntimeError, ValueError, TypeError, AttributeError):
                pass

        results: list[str] = []
        for v in data.get("webPages", {}).get("value", []):
            name = v.get("name", "Untitled Result")
            url = v.get("url", "#")
            snippet = v.get("snippet", "No snippet available.")
            results.append(f"### {name}\nURL: {url}\n{snippet}\n")
        return results

    @staticmethod
    def parse_google_results(data: dict[str, Any]) -> list[str]:
        """Parses Google Custom Search results into Markdown blocks."""
        if HAS_RUST and hasattr(rc, "parse_google_results_rust"):
            try:
                return rc.parse_google_results_rust(data)
            except (RuntimeError, ValueError, TypeError, AttributeError):
                pass
        results: list[str] = []
        for item in data.get("items", []):
            title = item.get("title", "Untitled Result")
            link = item.get("link", "#")
            snippet = item.get("snippet", "No snippet available.")
            results.append(f"### {title}\nURL: {link}\n{snippet}\n")
        return results

    @staticmethod
    def parse_ddg_results(data: list[dict[str, Any]]) -> list[str]:
        """Parses DuckDuckGo results from ddg_search library format."""
        if HAS_RUST and hasattr(rc, "parse_ddg_results_rust"):
            try:
                return rc.parse_ddg_results_rust(data)
            except (RuntimeError, ValueError, TypeError, AttributeError):
                pass
        results: list[str] = []
        for r in data:
            title = r.get("title", "Untitled Result")
            href = r.get("href", "#")
            body = r.get("body", "No description available.")
            results.append(f"### {title}\nURL: {href}\n{body}\n")
        return results

    @staticmethod
    def format_results_block(results: list[str], provider: str) -> str:
        """Combines list of results into a single string with provider indicator."""
        if not results:
            return f"No {provider} results found."
        return "\n".join(results)
