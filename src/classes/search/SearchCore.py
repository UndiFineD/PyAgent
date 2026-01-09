#!/usr/bin/env python3

"""
SearchCore logic for PyAgent.
Pure logic for parsing search results from various providers.
No I/O or side effects.
"""

from typing import List, Dict, Any, Optional

class SearchCore:
    """Pure logic core for search result processing."""

    @staticmethod
    def parse_bing_results(data: Dict[str, Any]) -> List[str]:
        """Parses Bing web search results into Markdown blocks."""
        results: List[str] = []
        for v in data.get("webPages", {}).get("value", []):
            name = v.get("name", "Untitled Result")
            url = v.get("url", "#")
            snippet = v.get("snippet", "No snippet available.")
            results.append(f"### {name}\nURL: {url}\n{snippet}\n")
        return results

    @staticmethod
    def parse_google_results(data: Dict[str, Any]) -> List[str]:
        """Parses Google Custom Search results into Markdown blocks."""
        results: List[str] = []
        for item in data.get("items", []):
            title = item.get("title", "Untitled Result")
            link = item.get("link", "#")
            snippet = item.get("snippet", "No snippet available.")
            results.append(f"### {title}\nURL: {link}\n{snippet}\n")
        return results

    @staticmethod
    def parse_ddg_results(data: List[Dict[str, Any]]) -> List[str]:
        """Parses DuckDuckGo results from ddg_search library format."""
        results: List[str] = []
        for r in data:
            title = r.get("title", "Untitled Result")
            href = r.get("href", "#")
            body = r.get("body", "No description available.")
            results.append(f"### {title}\nURL: {href}\n{body}\n")
        return results

    @staticmethod
    def format_results_block(results: List[str], provider: str) -> str:
        """Combines list of results into a single string with a provider-specific indicator."""
        if not results:
            return f"No {provider} results found."
        return "\n".join(results)
