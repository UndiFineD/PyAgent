r"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/jsontree/mapping.description.md

# mapping

**File**: `src\core\base\utils\jsontree\mapping.py`  
**Type**: Python Module  
**Summary**: 0 classes, 6 functions, 8 imports  
**Lines**: 77  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for mapping.

## Functions (6)

### `json_map_leaves(func, value)`

### `json_map_leaves(func, value)`

### `json_map_leaves(func, value)`

### `json_map_leaves(func, value)`

### `json_map_leaves(func, value)`

Apply a function to each leaf in a nested JSON structure.

Preserves the structure of the input, replacing each leaf with
the result of applying func to it.

Args:
    func: Function to apply to each leaf value.
    value: A nested JSON structure.
    
Returns:
    A new structure with the same shape, but with transformed leaves.

### `json_map_leaves_async(func, value)`

Apply a function to each leaf (async-ready version).

Same as json_map_leaves but can be used with async functions
when combined with asyncio.gather.

Args:
    func: Function to apply to each leaf value.
    value: A nested JSON structure.
    
Returns:
    A new structure with transformed leaves.

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `src.core.base.utils.jsontree.types.JSONTree`
- `src.core.base.utils.jsontree.types._JSONTree`
- `src.core.base.utils.jsontree.types._T`
- `src.core.base.utils.jsontree.types._U`
- `typing.Any`
- `typing.Callable`
- `typing.overload`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/jsontree/mapping.improvements.md

# Improvements for mapping

**File**: `src\core\base\utils\jsontree\mapping.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 77 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `mapping_test.py` with pytest tests

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
