#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/SharedContext.description.md

# SharedContext

**File**: `src\classes\context\SharedContext.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 36  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `SharedContext`

Context shared with team members.

Attributes:
    context_id: Unique identifier.
    owner: Owner username.
    shared_with: List of usernames shared with.
    permission: Permission level.
    last_sync: Last synchronization timestamp.

## Dependencies

**Imports** (18):
- `SharingPermission.SharingPermission`
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
- ... and 3 more

---
*Auto-generated documentation*
## Source: src-old/classes/context/SharedContext.improvements.md

# Improvements for SharedContext

**File**: `src\classes\context\SharedContext.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 36 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SharedContext_test.py` with pytest tests

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

from .SharingPermission import SharingPermission


@dataclass
class SharedContext:
    """Context shared with team members.

    Attributes:
        context_id: Unique identifier.
        owner: Owner username.
        shared_with: List of usernames shared with.
        permission: Permission level.
        last_sync: Last synchronization timestamp.

    """

    context_id: str
    owner: str
    shared_with: List[str] = field(default_factory=lambda: [])
    permission: SharingPermission = SharingPermission.READ_ONLY
    last_sync: str = ""
