#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/VisualizationType.description.md

# VisualizationType

**File**: `src\classes\context\VisualizationType.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 24  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `VisualizationType`

**Inherits from**: Enum

Types of context visualization.

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `hashlib`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `src.classes.base_agent.BaseAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 2 more

---
*Auto-generated documentation*
## Source: src-old/classes/context/VisualizationType.improvements.md

# Improvements for VisualizationType

**File**: `src\classes\context\VisualizationType.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 24 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `VisualizationType_test.py` with pytest tests

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

"""Auto-extracted class from agent_context.py"""


from enum import Enum


class VisualizationType(Enum):
    """Types of context visualization."""

    DEPENDENCY_GRAPH = "dependency_graph"
    CALL_HIERARCHY = "call_hierarchy"
    FILE_TREE = "file_tree"
    MIND_MAP = "mind_map"
