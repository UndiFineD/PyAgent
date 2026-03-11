#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/ContextTemplate.description.md

# ContextTemplate

**File**: `src\classes\context\ContextTemplate.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 26  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextTemplate`

Template for context documentation.

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
## Source: src-old/classes/context/ContextTemplate.improvements.md

# Improvements for ContextTemplate

**File**: `src\classes\context\ContextTemplate.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 26 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextTemplate_test.py` with pytest tests

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

"""Auto-extracted class from agent_context.py"""


from dataclasses import dataclass, field
from typing import List


@dataclass
class ContextTemplate:
    """Template for context documentation."""

    name: str
    file_type: str
    sections: List[str]
    template_content: str
    required_fields: List[str] = field(default_factory=lambda: [])
