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
SearchCore logic for PyAgent.
Pure logic for parsing search results from various providers.
No I/O or side effects.
"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from typing import Any

try:
    import rust_core as rc

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION


class SearchCore:
    """Pure logic core for search result processing."""

    @staticmethod
    def parse_bing_results(data: dict[str, Any]) -> list[str]:
        """Parses Bing web search results into Markdown blocks."""
        if HAS_RUST:
            try:
                return rc.parse_bing_results(data)  # type: ignore[attr-defined]
            except Exception:
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
        if HAS_RUST:
            try:
                return rc.parse_google_results(data)  # type: ignore[attr-defined]
            except Exception:
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
        if HAS_RUST:
            try:
                return rc.parse_ddg_results(data)  # type: ignore[attr-defined]
            except Exception:
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
        """Combines list of results into a single string with a provider-specific indicator."""
        if HAS_RUST:
            try:
                return rc.format_results_block(results, provider)  # type: ignore[attr-defined]
            except Exception:
                pass
        if not results:
            return f"No {provider} results found."
        return "\n".join(results)
