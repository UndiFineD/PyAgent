#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/swarm/MergeConflictMixin.description.md

# MergeConflictMixin

**File**: `src\\logic\agents\\swarm\\MergeConflictMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 79  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for MergeConflictMixin.

## Classes (1)

### `MergeConflictMixin`

Mixin for handling merge conflicts in file content.

**Methods** (2):
- `detect_merge_conflicts(self, content)`
- `resolve_merge_conflict(self, content, resolution)`

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/swarm/MergeConflictMixin.improvements.md

# Improvements for MergeConflictMixin

**File**: `src\\logic\agents\\swarm\\MergeConflictMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 79 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MergeConflictMixin_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
from typing import Any


class MergeConflictMixin:
    """Mixin for handling merge conflicts in file content."""

    def detect_merge_conflicts(self, content: str) -> list[dict[str, Any]]:
        """Detect merge conflict markers in the content."""
        conflicts: list[dict[str, Any]] = []
        lines = content.split("\n")
        in_conflict = False
        conflict_start = 0
        ours: list[str] = []
        theirs: list[str] = []
        for i, line in enumerate(lines):
            if line.startswith("<<<<<<<"):
                in_conflict = True
                conflict_start = i
                ours = []
            elif line.startswith("=======") and in_conflict:
                pass  # Separator
            elif line.startswith(">>>>>>>") and in_conflict:
                conflicts.append(
                    {
                        "start_line": conflict_start,
                        "end_line": i,
                        "ours": "\n".join(ours),
                        "theirs": "\n".join(theirs),
                    }
                )
                in_conflict = False
                ours = []
                theirs = []
            elif in_conflict:
                # Optimized conflict parsing
                if "=======" not in content[content.find("<<<<<<<", conflict_start) : content.find(line, conflict_start)]:
                    ours.append(line)
                else:
                    theirs.append(line)
        return conflicts

    def resolve_merge_conflict(self, content: str, resolution: str = "ours") -> str:
        """Resolve merge conflicts in the content."""
        result: list[str] = []
        lines = content.split("\n")
        in_conflict = False
        ours_section = True
        ours: list[str] = []
        theirs: list[str] = []

        for line in lines:
            if line.startswith("<<<<<<<"):
                in_conflict = True
                ours_section = True
                ours = []
                theirs = []
            elif line.startswith("=======") and in_conflict:
                ours_section = False
            elif line.startswith(">>>>>>>") and in_conflict:
                # Apply resolution
                if resolution == "ours":
                    result.extend(ours)
                elif resolution == "theirs":
                    result.extend(theirs)
                else:
                    result.extend(ours)
                    result.extend(theirs)
                in_conflict = False
            elif in_conflict:
                if ours_section:
                    ours.append(line)
                else:
                    theirs.append(line)
            else:
                result.append(line)
        return "\n".join(result)
