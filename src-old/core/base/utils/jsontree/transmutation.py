r"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/jsontree/transmutation.description.md

# transmutation

**File**: `src\core\base\utils\jsontree\transmutation.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 5 imports  
**Lines**: 70  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for transmutation.

## Functions (2)

### `json_flatten(value, separator, list_separator)`

Flatten a nested JSON structure to a single-level dict with dot-notation keys.

### `json_unflatten(flat, separator)`

Reconstruct a nested JSON structure from a flattened dict.

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `src.core.base.utils.jsontree.path._parse_path`
- `src.core.base.utils.jsontree.types.JSONTree`
- `src.core.base.utils.jsontree.types._T`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/jsontree/transmutation.improvements.md

# Improvements for transmutation

**File**: `src\core\base\utils\jsontree\transmutation.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 70 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `transmutation_test.py` with pytest tests

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
