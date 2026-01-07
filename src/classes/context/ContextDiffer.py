#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from .ContextDiff import ContextDiff

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import re
import zlib

class ContextDiffer:
    """Shows changes in context between versions.

    Provides detailed diff visualization between context versions.

    Example:
        >>> differ=ContextDiffer()
        >>> diff=differ.diff_versions(old_content, new_content)
    """

    def __init__(self) -> None:
        """Initialize context differ."""
        self.diffs: List[str] = []

    def compute_diff(self, content_from: str, content_to: str) -> ContextDiff:
        """Compute a structured diff between two context contents."""
        return self.diff_versions(content_from, content_to)

    def get_section_changes(self, content_from: str, content_to: str) -> Dict[str, List[str]]:
        """Return section-level changes between two contents."""
        diff = self.diff_versions(content_from, content_to)
        return {
            "added": diff.added_sections,
            "removed": diff.removed_sections,
            "modified": diff.modified_sections,
        }

    def summarize_diff(self, diff: ContextDiff) -> str:
        """Summarize a ContextDiff into a human-readable sentence."""
        return diff.change_summary or (
            f"Added {len(diff.added_sections)}, removed {len(diff.removed_sections)}, "
            f"modified {len(diff.modified_sections)} sections"
        )

    def diff_versions(
        self,
        content_from: str,
        content_to: str,
        version_from: str = "v1",
        version_to: str = "v2"
    ) -> ContextDiff:
        """Create diff between two content versions.

        Args:
            content_from: Original content.
            content_to: New content.
            version_from: Source version label.
            version_to: Target version label.

        Returns:
            ContextDiff with changes.
        """
        # Extract sections
        sections_from: set[str] = set(re.findall(r"##\s+(\w+)", content_from))
        sections_to: set[str] = set(re.findall(r"##\s+(\w+)", content_to))
        added: List[str] = list(sections_to - sections_from)
        removed: List[str] = list(sections_from - sections_to)
        modified: List[str] = []
        # Check for modified content in common sections
        common = sections_from & sections_to
        for section in common:
            if content_from.count(section) != content_to.count(section):
                modified.append(section)
        return ContextDiff(
            version_from=version_from,
            version_to=version_to,
            added_sections=added,
            removed_sections=removed,
            modified_sections=modified,
            change_summary=(
                f"Added {len(added)}, removed {len(removed)}, "
                f"modified {len(modified)} sections"
            ))
