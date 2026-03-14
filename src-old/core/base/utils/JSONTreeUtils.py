r"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/JSONTreeUtils.description.md

# JSONTreeUtils

**File**: `src\core\base\utils\JSONTreeUtils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 19 imports  
**Lines**: 70  
**Complexity**: 0 (simple)

## Overview

JSONTreeUtils - Nested JSON traversal and transformation utilities.

Refactored to modular package structure for Phase 317.
Original monolithic implementation delegated to src.core.base.utils.jsontree modules.

## Dependencies

**Imports** (19):
- `src.core.base.utils.jsontree.iteration.json_iter_leaves`
- `src.core.base.utils.jsontree.iteration.json_iter_leaves_with_path`
- `src.core.base.utils.jsontree.mapping.json_map_leaves`
- `src.core.base.utils.jsontree.mapping.json_map_leaves_async`
- `src.core.base.utils.jsontree.meta.json_count_leaves`
- `src.core.base.utils.jsontree.meta.json_depth`
- `src.core.base.utils.jsontree.meta.json_filter_leaves`
- `src.core.base.utils.jsontree.meta.json_find_leaves`
- `src.core.base.utils.jsontree.meta.json_validate_leaves`
- `src.core.base.utils.jsontree.path.json_get_path`
- `src.core.base.utils.jsontree.path.json_set_path`
- `src.core.base.utils.jsontree.reduction.json_reduce_leaves`
- `src.core.base.utils.jsontree.rust.RUST_ACCELERATION_AVAILABLE`
- `src.core.base.utils.jsontree.rust.json_count_leaves_fast`
- `src.core.base.utils.jsontree.rust.json_flatten_fast`
- ... and 4 more

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/JSONTreeUtils.improvements.md

# Improvements for JSONTreeUtils

**File**: `src\core\base\utils\JSONTreeUtils.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 70 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `JSONTreeUtils_test.py` with pytest tests

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
