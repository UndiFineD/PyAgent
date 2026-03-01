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
