#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from .SearchResult import SearchResult

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re

class ChangelogSearcher:
    """Searches changelog content across project history.

    Provides search functionality for finding specific entries
    in changelog history.

    Example:
        >>> searcher=ChangelogSearcher()
        >>> results=searcher.search("bug fix", changelog_content)
    """

    def search(self, query: str, content: str) -> List[SearchResult]:
        """Search for query in changelog content.

        Args:
            query: Search query string.
            content: Changelog content to search.

        Returns:
            List of search results.
        """
        results: List[SearchResult] = []
        lines = content.split('\n')
        current_version = "Unknown"
        for i, line in enumerate(lines, 1):
            # Track current version
            version_match = re.match(r"##\s*\[?(\d+\.\d+\.\d+|\d{4}\.\d{2}\.\d{2})\]?", line)
            if version_match:
                current_version = version_match.group(1)
            # Search for query
            if query.lower() in line.lower():
                results.append(SearchResult(
                    version=current_version,
                    line_number=i,
                    context=line.strip(),
                    match_score=self._calculate_score(query, line)
                ))
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
        if re.search(rf'\b{re.escape(query_lower)}\b', text_lower):
            return 0.8
        # Substring match
        return 0.5
