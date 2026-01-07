#!/usr/bin/env python3

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from .BlameInfo import BlameInfo
from .ErrorEntry import ErrorEntry

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import json
import logging
import re
import subprocess

class BlameTracker:
    """Tracks git blame information for errors.

    Uses git integration to identify who introduced errors
    and when.

    Attributes:
        blame_cache: Cache of blame information.
    """

    def __init__(self) -> None:
        """Initialize the blame tracker."""
        self.blame_cache: Dict[str, BlameInfo] = {}

    def get_blame(self, error: ErrorEntry) -> BlameInfo:
        """Get blame information for an error.

        Args:
            error: The error to get blame for.

        Returns:
            BlameInfo with commit and author details.
        """
        cache_key = f"{error.file_path}:{error.line_number}"
        if cache_key in self.blame_cache:
            return self.blame_cache[cache_key]

        blame_info = BlameInfo(error_id=error.id)

        try:
            result = subprocess.run(
                ["git", "blame", "-L",
                 f"{error.line_number},{error.line_number}",
                 "--porcelain", error.file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                blame_info = self._parse_blame_output(
                    error.id, result.stdout
                )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        self.blame_cache[cache_key] = blame_info
        return blame_info

    def _parse_blame_output(
        self, error_id: str, output: str
    ) -> BlameInfo:
        """Parse git blame output."""
        lines = output.strip().split('\n')
        info = BlameInfo(error_id=error_id)

        if lines:
            parts = lines[0].split()
            if parts:
                info.commit_hash = parts[0]

        for line in lines:
            if line.startswith("author "):
                info.author = line[7:]
            elif line.startswith("author-time "):
                timestamp = int(line[12:])
                info.commit_date = datetime.fromtimestamp(
                    timestamp
                ).isoformat()
            elif line.startswith("summary "):
                info.commit_message = line[8:]

        return info

    def get_top_contributors(
        self, errors: List[ErrorEntry], limit: int = 5
    ) -> List[Tuple[str, int]]:
        """Get top contributors to errors.

        Args:
            errors: List of errors to analyze.
            limit: Maximum number of contributors to return.

        Returns:
            List of (author, count) tuples.
        """
        author_counts: Dict[str, int] = {}
        for error in errors:
            blame = self.get_blame(error)
            if blame.author:
                author_counts[blame.author] = (
                    author_counts.get(blame.author, 0) + 1
                )

        sorted_authors = sorted(
            author_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_authors[:limit]
