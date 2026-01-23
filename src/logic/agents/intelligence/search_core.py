"""
SearchCore logic for PyAgent.
(Facade for src.core.base.common.search_core)
"""

from __future__ import annotations
import logging
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
        if HAS_RUST and hasattr(rc, "parse_google_results_rust"):
            try:
                return rc.parse_google_results_rust(data)
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
        if HAS_RUST and hasattr(rc, "parse_ddg_results_rust"):
            try:
                return rc.parse_ddg_results_rust(data)
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
        """Combines list of results into a single string with provider indicator."""
        if not results:
            return f"No {provider} results found."
        return "\n".join(results)
