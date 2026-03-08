"""
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

"""
JSONTreeUtils - Nested JSON traversal and transformation utilities.

Refactored to modular package structure for Phase 317.
Original monolithic implementation delegated to src.core.base.utils.jsontree modules.
"""

from src.core.base.utils.jsontree.types import JSONTree
from src.core.base.utils.jsontree.iteration import (
    json_iter_leaves,
    json_iter_leaves_with_path,
)
from src.core.base.utils.jsontree.mapping import (
    json_map_leaves,
    json_map_leaves_async,
)
from src.core.base.utils.jsontree.reduction import json_reduce_leaves
from src.core.base.utils.jsontree.meta import (
    json_count_leaves,
    json_depth,
    json_filter_leaves,
    json_validate_leaves,
    json_find_leaves,
)
from src.core.base.utils.jsontree.transmutation import (
    json_flatten,
    json_unflatten,
)
from src.core.base.utils.jsontree.path import (
    json_get_path,
    json_set_path,
)
from src.core.base.utils.jsontree.rust import (
    json_iter_leaves_fast,
    json_count_leaves_fast,
    json_flatten_fast,
    RUST_ACCELERATION_AVAILABLE,
)

__all__ = [
    # Type aliases
    "JSONTree",
    # Iteration
    "json_iter_leaves",
    "json_iter_leaves_with_path",
    "json_iter_leaves_fast",
    # Mapping
    "json_map_leaves",
    "json_map_leaves_async",
    # Reduction
    "json_reduce_leaves",
    # Counting
    "json_count_leaves",
    "json_count_leaves_fast",
    "json_depth",
    # Flattening
    "json_flatten",
    "json_flatten_fast",
    "json_unflatten",
    # Path access
    "json_get_path",
    "json_set_path",
    # Filtering
    "json_filter_leaves",
    # Validation
    "json_validate_leaves",
    "json_find_leaves",
    # Constants
    "RUST_ACCELERATION_AVAILABLE",
]
