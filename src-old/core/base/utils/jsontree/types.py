"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/jsontree/types.description.md

# types

**File**: `src\core\base\utils\jsontree\types.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 4 imports  
**Lines**: 21  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for types.

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `typing.Any`
- `typing.TypeAlias`
- `typing.TypeVar`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/jsontree/types.improvements.md

# Improvements for types

**File**: `src\core\base\utils\jsontree\types.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 21 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `types_test.py` with pytest tests

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
from typing import TypeVar, TypeAlias, Any

_T = TypeVar("_T")
_U = TypeVar("_U")

# Type alias for nested JSON structures where leaves can be any type
JSONTree: TypeAlias = (
    dict[str, "JSONTree[_T]"] | list["JSONTree[_T]"] | tuple["JSONTree[_T]", ...] | _T
)

# Extended type alias for overload compatibility
_JSONTree: TypeAlias = (
    dict[str, "JSONTree[_T]"]
    | list["JSONTree[_T]"]
    | tuple["JSONTree[_T]", ...]
    | dict[str, _T]
    | list[_T]
    | tuple[_T, ...]
    | _T
)
