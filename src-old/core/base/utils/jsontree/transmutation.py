"""
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
from typing import Any
from src.core.base.utils.jsontree.types import JSONTree, _T
from src.core.base.utils.jsontree.path import _parse_path


def json_flatten(
    value: JSONTree[_T],
    separator: str = ".",
    list_separator: str = "",
) -> dict[str, _T]:
    """
    Flatten a nested JSON structure to a single-level dict with dot-notation keys.
    """
    result: dict[str, _T] = {}

    def _flatten(obj: Any, prefix: str = "") -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{prefix}{separator}{k}" if prefix else k
                _flatten(v, new_key)
        elif isinstance(obj, (list, tuple)):
            for i, v in enumerate(obj):
                if list_separator:
                    new_key = f"{prefix}{list_separator}{i}"
                else:
                    new_key = f"{prefix}[{i}]"
                _flatten(v, new_key)
        else:
            result[prefix] = obj

    _flatten(value)
    return result


def json_unflatten(
    flat: dict[str, _T],
    separator: str = ".",
) -> dict[str, Any]:
    """
    Reconstruct a nested JSON structure from a flattened dict.
    """
    result: dict[str, Any] = {}

    for key, value in flat.items():
        parts = _parse_path(key, separator)
        current = result

        for i, part in enumerate(parts[:-1]):
            next_part = parts[i + 1]

            if isinstance(part, int):
                while len(current) <= part:
                    current.append(None)
                if current[part] is None:
                    current[part] = [] if isinstance(next_part, int) else {}
                current = current[part]
            else:
                if part not in current:
                    current[part] = [] if isinstance(next_part, int) else {}
                current = current[part]

        final_part = parts[-1]
        if isinstance(final_part, int):
            while len(current) <= final_part:
                current.append(None)
            current[final_part] = value
        else:
            current[final_part] = value

    return result
