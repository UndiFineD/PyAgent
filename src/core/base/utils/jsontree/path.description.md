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
