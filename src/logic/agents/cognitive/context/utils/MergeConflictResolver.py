#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from src.logic.agents.cognitive.context.utils.ConflictResolution import ConflictResolution
from src.logic.agents.cognitive.context.models.MergeConflict import MergeConflict

from src.core.base.BaseAgent import BaseAgent
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

class MergeConflictResolver:
    """Resolves merge conflicts in context files.

    Provides strategies for resolving conflicts during context merges.

    Example:
        >>> resolver=MergeConflictResolver()
        >>> resolved=resolver.resolve(conflict, ConflictResolution.OURS)
    """

    def __init__(self, strategy: ConflictResolution = ConflictResolution.AUTO) -> None:
        self.strategy: ConflictResolution = strategy

    def set_strategy(self, strategy: ConflictResolution) -> None:
        self.strategy = strategy

    def detect_conflicts(self, ours: str, theirs: Optional[str] = None) -> List[MergeConflict]:
        """Detect merge conflicts.

        Supports two modes:
        - detect_conflicts(content_with_markers)
        - detect_conflicts(ours, theirs)
        """
        if theirs is None:
            content = ours
            conflicts: List[MergeConflict] = []
            pattern = r"<<<<<<<[^\n]*\n(.*?)\n=======\n(.*?)\n>>>>>>>"
            for match in re.finditer(pattern, content, re.DOTALL):
                conflicts.append(MergeConflict(
                    section="conflict",
                    ours=match.group(1),
                    theirs=match.group(2)
                ))
            return conflicts

        if ours == theirs:
            return []

        def _section_name(text: str) -> str:
            first = text.strip().splitlines()[0] if text.strip() else ""
            if first.startswith("##"):
                return first.lstrip("#").strip() or "section"
            return "content"

        return [MergeConflict(section=_section_name(ours), ours=ours, theirs=theirs)]

    def resolve(self, conflict: MergeConflict, strategy: Optional[ConflictResolution] = None) -> str:
        """Resolve a merge conflict.

        Args:
            conflict: Conflict to resolve.
            strategy: Optional resolution strategy (defaults to current strategy).

        Returns:
            Resolved content.
        """
        effective = strategy or self.strategy
        if effective == ConflictResolution.OURS:
            conflict.resolution = effective
            return conflict.ours
        if effective == ConflictResolution.THEIRS:
            conflict.resolution = effective
            return conflict.theirs
        if effective == ConflictResolution.AUTO:
            # Auto: prefer longer content
            conflict.resolution = effective
            return conflict.ours if len(conflict.ours) >= len(conflict.theirs) else conflict.theirs

        conflict.resolution = ConflictResolution.MANUAL
        return f"MANUAL RESOLUTION NEEDED:\n{conflict.ours}\n---\n{conflict.theirs}"

    def resolve_all(
        self,
        conflicts: List[MergeConflict],
        strategy: Optional[ConflictResolution] = None,
    ) -> str:
        """Resolve all conflicts and join results."""
        return "\n".join(self.resolve(c, strategy=strategy) for c in conflicts)
