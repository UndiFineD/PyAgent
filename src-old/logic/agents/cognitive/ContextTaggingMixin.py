#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/ContextTaggingMixin.description.md

# ContextTaggingMixin

**File**: `src\\logic\agents\\cognitive\\ContextTaggingMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 35  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for ContextTaggingMixin.

## Classes (1)

### `ContextTaggingMixin`

Tagging methods for ContextAgent.

**Methods** (5):
- `add_tag(self, tag)`
- `remove_tag(self, tag_name)`
- `get_tags(self)`
- `has_tag(self, tag_name)`
- `get_tags_by_parent(self, parent_name)`

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `src.logic.agents.cognitive.context.models.ContextTag.ContextTag`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/ContextTaggingMixin.improvements.md

# Improvements for ContextTaggingMixin

**File**: `src\\logic\agents\\cognitive\\ContextTaggingMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 35 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextTaggingMixin_test.py` with pytest tests

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
# Licensed under the Apache License, Version 2.0 (the "License");
from src.logic.agents.cognitive.context.models.ContextTag import ContextTag


class ContextTaggingMixin:
    """Tagging methods for ContextAgent."""

    def add_tag(self, tag: ContextTag) -> None:
        """Add a tag."""
        if not hasattr(self, "_tags"):
            self._tags: dict[str, ContextTag] = {}
        self._tags[tag.name] = tag

    def remove_tag(self, tag_name: str) -> bool:
        """Remove a tag."""
        if hasattr(self, "_tags") and tag_name in self._tags:
            del self._tags[tag_name]
            return True
        return False

    def get_tags(self) -> list[ContextTag]:
        """Get all tags."""
        return list(getattr(self, "_tags", {}).values())

    def has_tag(self, tag_name: str) -> bool:
        """Check if a tag exists."""
        return tag_name in getattr(self, "_tags", {})

    def get_tags_by_parent(self, parent_name: str) -> list[ContextTag]:
        """Get all tags with a specific parent."""
        return [t for t in getattr(self, "_tags", {}).values() if t.parent == parent_name]
