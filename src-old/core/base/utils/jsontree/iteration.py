r"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/jsontree/iteration.description.md

# iteration

**File**: `src\core\base\utils\jsontree\iteration.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 4 imports  
**Lines**: 50  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for iteration.

## Functions (2)

### `json_iter_leaves(value)`

Iterate through each leaf in a nested JSON structure.

A leaf is any value that is not a dict, list, or tuple.

Args:
    value: A nested JSON structure (dict, list, tuple, or leaf value).
    
Yields:
    Each leaf value in depth-first order.

### `json_iter_leaves_with_path(value, prefix)`

Iterate through each leaf with its dot-notation path.

Args:
    value: A nested JSON structure.
    prefix: Optional path prefix (used for recursion).
    
Yields:
    Tuples of (path, leaf_value).

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `collections.abc.Iterable`
- `src.core.base.utils.jsontree.types.JSONTree`
- `src.core.base.utils.jsontree.types._T`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/jsontree/iteration.improvements.md

# Improvements for iteration

**File**: `src\core\base\utils\jsontree\iteration.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 50 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `iteration_test.py` with pytest tests

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
