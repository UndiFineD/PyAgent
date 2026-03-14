r"""
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
