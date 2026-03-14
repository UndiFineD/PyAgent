r"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/jsontree/path.description.md

# path

**File**: `src\core\base\utils\jsontree\path.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 6 imports  
**Lines**: 104  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for path.

## Functions (3)

### `_parse_path(path, separator)`

Parse a dot-notation path into parts, handling array indices.

### `json_get_path(value, path, default, separator)`

Get a value from a nested structure using dot-notation path.

Args:
    value: A nested JSON structure.
    path: Dot-notation path (e.g., "a.b.c" or "a[0].b").
    default: Default value if path not found.
    separator: Separator for path parts.
    
Returns:
    The value at the path, or default if not found.

### `json_set_path(value, path, new_value, separator, create_missing)`

Set a value in a nested structure using dot-notation path.

Args:
    value: A nested JSON structure (will be modified in place).
    path: Dot-notation path (e.g., "a.b.c").
    new_value: Value to set at the path.
    separator: Separator for path parts.
    create_missing: Create intermediate dicts/lists if missing.
    
Returns:
    The modified structure.

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `re`
- `src.core.base.utils.jsontree.types.JSONTree`
- `src.core.base.utils.jsontree.types._T`
- `src.core.base.utils.jsontree.types._U`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/jsontree/path.improvements.md

# Improvements for path

**File**: `src\core\base\utils\jsontree\path.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 104 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `path_test.py` with pytest tests

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
