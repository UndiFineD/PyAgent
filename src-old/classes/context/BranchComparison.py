#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/BranchComparison.description.md

# BranchComparison

**File**: `src\classes\context\BranchComparison.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 35  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `BranchComparison`

Comparison of context across branches.

Attributes:
    branch_a: First branch name.
    branch_b: Second branch name.
    files_only_in_a: Files only in branch A.
    files_only_in_b: Files only in branch B.
    modified_files: Files modified between branches.

## Dependencies

**Imports** (18):
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
- ... and 3 more

---
*Auto-generated documentation*
## Source: src-old/classes/context/BranchComparison.improvements.md

# Improvements for BranchComparison

**File**: `src\classes\context\BranchComparison.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 35 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `BranchComparison_test.py` with pytest tests

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

from dataclasses import dataclass, field

"""Auto-extracted class from agent_context.py"""


from typing import List


@dataclass
class BranchComparison:
    """Comparison of context across branches.

    Attributes:
        branch_a: First branch name.
        branch_b: Second branch name.
        files_only_in_a: Files only in branch A.
        files_only_in_b: Files only in branch B.
        modified_files: Files modified between branches.

    """

    branch_a: str
    branch_b: str
    files_only_in_a: List[str] = field(default_factory=lambda: [])
    files_only_in_b: List[str] = field(default_factory=lambda: [])
    modified_files: List[str] = field(default_factory=lambda: [])
