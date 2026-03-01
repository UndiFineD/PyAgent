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
