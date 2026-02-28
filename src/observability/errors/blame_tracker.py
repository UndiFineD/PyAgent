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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

import subprocess
from datetime import datetime
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .blame_info import BlameInfo
from .error_entry import ErrorEntry

__version__ = VERSION


class BlameTracker:
    """Tracks git blame information for errors.

    Uses git integration to identify who introduced errors
    and when.

    Attributes:
        blame_cache: Cache of blame information.
    """

    def __init__(self, recorder: Any = None) -> None:
        """Initialize the blame tracker."""
        self.blame_cache: dict[str, BlameInfo] = {}
        self.recorder = recorder

    def _record(self, action: str, result: str) -> None:
        """Record blame operations."""
        if self.recorder:
            self.recorder.record_interaction("Git", "Blame", action, result)

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
                [
                    "git",
                    "blame",
                    "-L",
                    f"{error.line_number},{error.line_number}",
                    "--porcelain",
                    error.file_path,
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                blame_info = self._parse_blame_output(error.id, result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        self.blame_cache[cache_key] = blame_info
        return blame_info

    def _parse_blame_output(self, error_id: str, output: str) -> BlameInfo:
        """Parse git blame output."""
        lines = output.strip().split("\n")
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
                info.commit_date = datetime.fromtimestamp(timestamp).isoformat()
            elif line.startswith("summary "):
                info.commit_message = line[8:]

        return info

    def get_top_contributors(self, errors: list[ErrorEntry], limit: int = 5) -> list[tuple[str, int]]:
        """Get top contributors to errors.

        Args:
            errors: List of errors to analyze.
            limit: Maximum number of contributors to return.

        Returns:
            List of (author, count) tuples.
        """
        author_counts: dict[str, int] = {}
        for error in errors:
            blame = self.get_blame(error)
            if blame.author:
                author_counts[blame.author] = author_counts.get(blame.author, 0) + 1

        sorted_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_authors[:limit]
