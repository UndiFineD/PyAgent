"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/jsontree/reduction.description.md

# reduction

**File**: `src\core\base\utils\jsontree\reduction.py`  
**Type**: Python Module  
**Summary**: 0 classes, 6 functions, 9 imports  
**Lines**: 70  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for reduction.

## Functions (6)

### `json_reduce_leaves()`

### `json_reduce_leaves()`

### `json_reduce_leaves()`

### `json_reduce_leaves()`

### `json_reduce_leaves()`

### `json_reduce_leaves()`

Apply a function of two arguments cumulatively to each leaf.

Reduces all leaves to a single value, from left to right.

Args:
    func: A binary function (accumulator, leaf) -> result.
    value: A nested JSON structure.
    initial: Optional initial value for the reduction.
    
Returns:
    The reduced value.

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `functools.reduce`
- `src.core.base.utils.jsontree.iteration.json_iter_leaves`
- `src.core.base.utils.jsontree.types.JSONTree`
- `src.core.base.utils.jsontree.types._JSONTree`
- `src.core.base.utils.jsontree.types._T`
- `src.core.base.utils.jsontree.types._U`
- `typing.Callable`
- `typing.overload`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/jsontree/reduction.improvements.md

# Improvements for reduction

**File**: `src\core\base\utils\jsontree\reduction.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 70 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `reduction_test.py` with pytest tests

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
from typing import Callable, overload
from functools import reduce
from src.core.base.utils.jsontree.types import JSONTree, _JSONTree, _T, _U
from src.core.base.utils.jsontree.iteration import json_iter_leaves


@overload
def json_reduce_leaves(
    func: Callable[[_T, _T], _T],
    value: _T | dict[str, _T],
    /,
) -> _T: ...


@overload
def json_reduce_leaves(
    func: Callable[[_T, _T], _T],
    value: _T | list[_T],
    /,
) -> _T: ...


@overload
def json_reduce_leaves(
    func: Callable[[_T, _T], _T],
    value: _T | tuple[_T, ...],
    /,
) -> _T: ...


@overload
def json_reduce_leaves(
    func: Callable[[_T, _T], _T],
    value: JSONTree[_T],
    /,
) -> _T: ...


@overload
def json_reduce_leaves(
    func: Callable[[_U, _T], _U],
    value: JSONTree[_T],
    initial: _U,
    /,
) -> _U: ...


def json_reduce_leaves(
    func: Callable[[_T, _T], _T] | Callable[[_U, _T], _U],
    value: _JSONTree[_T],
    initial: _U = ...,  # type: ignore[assignment]
    /,
) -> _T | _U:
    """
    Apply a function of two arguments cumulatively to each leaf.

    Reduces all leaves to a single value, from left to right.

    Args:
        func: A binary function (accumulator, leaf) -> result.
        value: A nested JSON structure.
        initial: Optional initial value for the reduction.

    Returns:
        The reduced value.
    """
    if initial is ...:
        return reduce(func, json_iter_leaves(value))  # type: ignore

    return reduce(func, json_iter_leaves(value), initial)  # type: ignore
