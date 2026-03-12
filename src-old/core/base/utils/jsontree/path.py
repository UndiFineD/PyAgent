"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/jsontree/path.description.md

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
## Source: src-old/core/base/utils/jsontree/path.improvements.md

# Improvements for path

**File**: `src\core\base\utils\jsontree\path.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 104 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `path_test.py` with pytest tests

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

from __future__ import annotations
import re
from typing import Any
from src.core.base.utils.jsontree.types import JSONTree, _T, _U


def _parse_path(path: str, separator: str = ".") -> list[str | int]:
    """Parse a dot-notation path into parts, handling array indices."""
    parts: list[str | int] = []

    # Split by separator, but keep array indices
    for part in re.split(rf"(?<!\[){re.escape(separator)}", path):
        # Check for array indices
        match = re.match(r"^(.+?)\[(\d+)\]$", part)
        if match:
            parts.append(match.group(1))
            parts.append(int(match.group(2)))
        elif re.match(r"^\[(\d+)\]$", part):
            parts.append(int(part[1:-1]))
        else:
            parts.append(part)

    return parts


def json_get_path(
    value: JSONTree[_T],
    path: str,
    default: _U = None,  # type: ignore
    separator: str = ".",
) -> _T | _U:
    """
    Get a value from a nested structure using dot-notation path.

    Args:
        value: A nested JSON structure.
        path: Dot-notation path (e.g., "a.b.c" or "a[0].b").
        default: Default value if path not found.
        separator: Separator for path parts.

    Returns:
        The value at the path, or default if not found.
    """
    parts = _parse_path(path, separator)
    current: Any = value

    try:
        for part in parts:
            if isinstance(part, int):
                current = current[part]
            elif isinstance(current, dict):
                current = current[part]
            else:
                return default
        return current
    except (KeyError, IndexError, TypeError):
        return default


def json_set_path(
    value: dict[str, Any],
    path: str,
    new_value: _T,
    separator: str = ".",
    create_missing: bool = True,
) -> dict[str, Any]:
    """
    Set a value in a nested structure using dot-notation path.

    Args:
        value: A nested JSON structure (will be modified in place).
        path: Dot-notation path (e.g., "a.b.c").
        new_value: Value to set at the path.
        separator: Separator for path parts.
        create_missing: Create intermediate dicts/lists if missing.

    Returns:
        The modified structure.
    """
    parts = _parse_path(path, separator)
    current: Any = value

    for i, part in enumerate(parts[:-1]):
        next_part = parts[i + 1]

        if isinstance(part, int):
            while len(current) <= part:
                current.append(None)
            if current[part] is None and create_missing:
                current[part] = [] if isinstance(next_part, int) else {}
            current = current[part]
        else:
            if part not in current and create_missing:
                current[part] = [] if isinstance(next_part, int) else {}
            current = current[part]

    final_part = parts[-1]
    if isinstance(final_part, int):
        while len(current) <= final_part:
            current.append(None)
        current[final_part] = new_value
    else:
        current[final_part] = new_value

    return value
