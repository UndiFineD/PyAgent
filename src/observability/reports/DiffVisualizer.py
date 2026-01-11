#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_changes.py"""

from .DiffResult import DiffResult
from .DiffViewMode import DiffViewMode

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re


































from src.core.base.version import VERSION
__version__ = VERSION

class DiffVisualizer:
    """Visualizes changelog differences with multiple view modes.

    Provides side-by-side and unified diff views for changelog
    comparison.

    Example:
        >>> visualizer=DiffVisualizer()
        >>> result=visualizer.compare("old content", "new content")
        >>> html=visualizer.render_html(result, DiffViewMode.SIDE_BY_SIDE)
    """

    def compare(self, old_content: str, new_content: str) -> DiffResult:
        """Compare two changelog versions.

        Args:
            old_content: Original changelog content.
            new_content: New changelog content.

        Returns:
            DiffResult with comparison details.
        """
        old_lines = set(old_content.split('\n'))
        new_lines = set(new_content.split('\n'))

        additions = list(new_lines - old_lines)
        deletions = list(old_lines - new_lines)
        unchanged = len(old_lines & new_lines)

        total = len(old_lines | new_lines)
        similarity = (unchanged / total * 100) if total > 0 else 100.0

        return DiffResult(
            additions=additions,
            deletions=deletions,
            unchanged=unchanged,
            similarity_score=similarity
        )

    def render_html(self, result: DiffResult, mode: DiffViewMode) -> str:
        """Render diff result as HTML.

        Args:
            result: DiffResult to render.
            mode: Visualization mode.

        Returns:
            HTML string representation of the diff.
        """
        if mode == DiffViewMode.SIDE_BY_SIDE:
            return self._render_side_by_side(result)
        elif mode == DiffViewMode.INLINE:
            return self._render_inline(result)
        return self._render_unified(result)

    def _render_unified(self, result: DiffResult) -> str:
        """Render unified diff view."""
        lines: List[str] = []
        lines.append("<div class='diff-unified'>")
        for line in result.deletions:
            lines.append(f"<span class='deletion'>- {line}</span>")
        for line in result.additions:
            lines.append(f"<span class='addition'>+ {line}</span>")
        lines.append("</div>")
        return '\n'.join(lines)

    def _render_side_by_side(self, result: DiffResult) -> str:
        """Render side-by-side diff view."""
        return (
            f"<div class='diff-side-by-side'>Deletions: "
            f"{len(result.deletions)}, Additions: "
            f"{len(result.additions)}</div>"
        )

    def _render_inline(self, result: DiffResult) -> str:
        """Render inline diff view."""
        total_changes = len(result.deletions) + len(result.additions)
        return f"<div class='diff-inline'>Changes: {total_changes}</div>"
