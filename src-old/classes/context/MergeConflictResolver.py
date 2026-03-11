#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/MergeConflictResolver.description.md

# MergeConflictResolver

**File**: `src\classes\context\MergeConflictResolver.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 104  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `MergeConflictResolver`

Resolves merge conflicts in context files.

Provides strategies for resolving conflicts during context merges.

Example:
    >>> resolver=MergeConflictResolver()
    >>> resolved=resolver.resolve(conflict, ConflictResolution.OURS)

**Methods** (5):
- `__init__(self, strategy)`
- `set_strategy(self, strategy)`
- `detect_conflicts(self, ours, theirs)`
- `resolve(self, conflict, strategy)`
- `resolve_all(self, conflicts, strategy)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `re`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.models.MergeConflict.MergeConflict`
- `src.logic.agents.cognitive.context.utils.ConflictResolution.ConflictResolution`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/context/MergeConflictResolver.improvements.md

# Improvements for MergeConflictResolver

**File**: `src\classes\context\MergeConflictResolver.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 104 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MergeConflictResolver_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END

"""

from __future__ import annotations

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


"""Auto-extracted class from agent_context.py"""

import re

from src.core.base.version import VERSION
from src.logic.agents.cognitive.context.models.MergeConflict import MergeConflict
from src.logic.agents.cognitive.context.utils.ConflictResolution import (
    ConflictResolution,
)

__version__ = VERSION


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

    def detect_conflicts(
        self, ours: str, theirs: str | None = None
    ) -> list[MergeConflict]:
        """Detect merge conflicts.

        Supports two modes:
        - detect_conflicts(content_with_markers)
        - detect_conflicts(ours, theirs)
        """
        if theirs is None:
            content = ours
            conflicts: list[MergeConflict] = []
            pattern = r"<<<<<<<[^\n]*\n(.*?)\n=======\n(.*?)\n>>>>>>>"
            for match in re.finditer(pattern, content, re.DOTALL):
                conflicts.append(
                    MergeConflict(
                        section="conflict", ours=match.group(1), theirs=match.group(2)
                    )
                )
            return conflicts

        if ours == theirs:
            return []

        def _section_name(text: str) -> str:
            first = text.strip().splitlines()[0] if text.strip() else ""
            if first.startswith("##"):
                return first.lstrip("#").strip() or "section"
            return "content"

        return [MergeConflict(section=_section_name(ours), ours=ours, theirs=theirs)]

    def resolve(
        self, conflict: MergeConflict, strategy: ConflictResolution | None = None
    ) -> str:
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
            return (
                conflict.ours
                if len(conflict.ours) >= len(conflict.theirs)
                else conflict.theirs
            )

        conflict.resolution = ConflictResolution.MANUAL
        return f"MANUAL RESOLUTION NEEDED:\n{conflict.ours}\n---\n{conflict.theirs}"

    def resolve_all(
        self,
        conflicts: list[MergeConflict],
        strategy: ConflictResolution | None = None,
    ) -> str:
        """Resolve all conflicts and join results."""
        return "\n".join(self.resolve(c, strategy=strategy) for c in conflicts)
