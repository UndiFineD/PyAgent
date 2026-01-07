#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from .ReportComparison import ReportComparison

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, cast
import ast
import hashlib
import json
import logging
import re
import sys
import time

# Define AGENT_DIR for default parameter
AGENT_DIR = Path(__file__).resolve().parent.parent.parent  # src/

class ReportComparator:
    """Compares report versions to show differences.
    Attributes:
        reports_dir: Directory containing reports.
    """

    def __init__(self, reports_dir: Path = AGENT_DIR):
        """Initialize comparator.
        Args:
            reports_dir: Directory containing report files.
        """

        self.reports_dir = reports_dir

    def compare(self, old_path: str, new_path: str, old_content: str, new_content: str) -> ReportComparison:
        """Compare two report versions.
        Args:
            old_path: Path to old version.
            new_path: Path to new version.
            old_content: Previous report content.
            new_content: New report content.
        Returns:
            ReportComparison with differences.
        """

        old_items = self._extract_items(old_content)
        new_items = self._extract_items(new_content)
        old_set = set(old_items)
        new_set = set(new_items)
        added = list(new_set - old_set)
        removed = list(old_set - new_set)
        unchanged = len(old_set & new_set)
        return ReportComparison(
            old_path=old_path,
            new_path=new_path,
            added=added,
            removed=removed,
            changed=[],
            unchanged_count=unchanged
        )

    def _extract_items(self, content: str) -> List[str]:
        """Extract list items from markdown content."""

        items: List[str] = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                items.append(line)
        return items
