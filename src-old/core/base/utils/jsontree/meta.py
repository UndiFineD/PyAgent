"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/jsontree/meta.description.md

# meta

**File**: `src\core\base\utils\jsontree\meta.py`  
**Type**: Python Module  
**Summary**: 0 classes, 5 functions, 6 imports  
**Lines**: 81  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for meta.

## Functions (5)

### `json_count_leaves(value)`

Count the number of leaves in a nested JSON structure.

### `json_depth(value)`

Calculate the maximum depth of a nested JSON structure.

### `json_filter_leaves(predicate, value)`

Filter leaves in a nested structure, keeping only those matching predicate.

### `json_validate_leaves(validator, value)`

Check if all leaves in a structure satisfy a predicate.

### `json_find_leaves(predicate, value)`

Find all leaves matching a predicate, with their paths.

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.utils.jsontree.iteration.json_iter_leaves`
- `src.core.base.utils.jsontree.iteration.json_iter_leaves_with_path`
- `src.core.base.utils.jsontree.types.JSONTree`
- `src.core.base.utils.jsontree.types._T`
- `typing.Callable`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/jsontree/meta.improvements.md

# Improvements for meta

**File**: `src\core\base\utils\jsontree\meta.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 81 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `meta_test.py` with pytest tests

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
from typing import Callable
from src.core.base.utils.jsontree.types import JSONTree, _T
from src.core.base.utils.jsontree.iteration import (
    json_iter_leaves,
    json_iter_leaves_with_path,
)


def json_count_leaves(value: JSONTree[_T]) -> int:
    """Count the number of leaves in a nested JSON structure."""
    return sum(1 for _ in json_iter_leaves(value))


def json_depth(value: JSONTree[_T]) -> int:
    """Calculate the maximum depth of a nested JSON structure."""
    if isinstance(value, dict):
        if not value:
            return 1
        return 1 + max(json_depth(v) for v in value.values())
    elif isinstance(value, (list, tuple)):
        if not value:
            return 1
        return 1 + max(json_depth(v) for v in value)
    else:
        return 0


def json_filter_leaves(
    predicate: Callable[[_T], bool],
    value: JSONTree[_T],
) -> JSONTree[_T]:
    """Filter leaves in a nested structure, keeping only those matching predicate."""
    if isinstance(value, dict):
        result = {}
        for k, v in value.items():
            filtered = json_filter_leaves(predicate, v)
            if isinstance(filtered, dict) and not filtered:
                continue
            if isinstance(filtered, (list, tuple)) and not filtered:
                continue
            result[k] = filtered
        return result
    elif isinstance(value, list):
        result_list = []
        for v in value:
            filtered = json_filter_leaves(predicate, v)
            if isinstance(filtered, dict) and not filtered:
                continue
            if isinstance(filtered, (list, tuple)) and not filtered:
                continue
            result_list.append(filtered)
        return result_list
    elif isinstance(value, tuple):
        result_tuple = []
        for v in value:
            filtered = json_filter_leaves(predicate, v)
            if isinstance(filtered, dict) and not filtered:
                continue
            if isinstance(filtered, (list, tuple)) and not filtered:
                continue
            result_tuple.append(filtered)
        return tuple(result_tuple)
    else:
        return value if predicate(value) else {}  # type: ignore


def json_validate_leaves(
    validator: Callable[[_T], bool],
    value: JSONTree[_T],
) -> bool:
    """Check if all leaves in a structure satisfy a predicate."""
    return all(validator(leaf) for leaf in json_iter_leaves(value))


def json_find_leaves(
    predicate: Callable[[_T], bool],
    value: JSONTree[_T],
) -> list[tuple[str, _T]]:
    """Find all leaves matching a predicate, with their paths."""
    return [
        (path, leaf)
        for path, leaf in json_iter_leaves_with_path(value)
        if predicate(leaf)
    ]
