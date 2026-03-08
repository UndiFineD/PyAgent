"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/jsontree/rust.description.md

# rust

**File**: `src\core\base\utils\jsontree\rust.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 12 imports  
**Lines**: 58  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for rust.

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `collections.abc.Iterable`
- `logging`
- `rust_core.json_count_leaves_rust`
- `rust_core.json_flatten_rust`
- `rust_core.json_iter_leaves_rust`
- `rust_core.json_map_leaves_rust`
- `src.core.base.utils.jsontree.iteration.json_iter_leaves`
- `src.core.base.utils.jsontree.meta.json_count_leaves`
- `src.core.base.utils.jsontree.transmutation.json_flatten`
- `src.core.base.utils.jsontree.types.JSONTree`
- `src.core.base.utils.jsontree.types._T`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/jsontree/rust.improvements.md

# Improvements for rust

**File**: `src\core\base\utils\jsontree\rust.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 58 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `rust_test.py` with pytest tests

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
import logging
from collections.abc import Iterable
from src.core.base.utils.jsontree.types import JSONTree, _T
from src.core.base.utils.jsontree.iteration import json_iter_leaves
from src.core.base.utils.jsontree.meta import json_count_leaves
from src.core.base.utils.jsontree.transmutation import json_flatten

logger = logging.getLogger(__name__)

# Try to import Rust-accelerated versions
try:
    from rust_core import (
        json_iter_leaves_rust,
        json_map_leaves_rust,
        json_count_leaves_rust,
        json_flatten_rust,
    )

    # Use Rust versions if available
    _json_iter_leaves_native = json_iter_leaves
    _json_count_leaves_native = json_count_leaves
    _json_flatten_native = json_flatten

    def json_iter_leaves_fast(value: JSONTree[_T]) -> Iterable[_T]:
        """Rust-accelerated leaf iteration."""
        try:
            return json_iter_leaves_rust(value)
        except Exception:
            return _json_iter_leaves_native(value)

    def json_count_leaves_fast(value: JSONTree[_T]) -> int:
        """Rust-accelerated leaf counting."""
        try:
            return json_count_leaves_rust(value)
        except Exception:
            return _json_count_leaves_native(value)

    def json_flatten_fast(
        value: JSONTree[_T],
        separator: str = ".",
    ) -> dict[str, _T]:
        """Rust-accelerated flattening."""
        try:
            return json_flatten_rust(value, separator)
        except Exception:
            return _json_flatten_native(value, separator)

    RUST_ACCELERATION_AVAILABLE = True
    logger.debug("JSONTreeUtils: Rust acceleration available")

except ImportError:
    # Rust not available, use pure Python
    json_iter_leaves_fast = json_iter_leaves
    json_count_leaves_fast = json_count_leaves
    json_flatten_fast = json_flatten
    RUST_ACCELERATION_AVAILABLE = False
    logger.debug("JSONTreeUtils: Using pure Python (Rust not available)")
