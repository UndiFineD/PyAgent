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
