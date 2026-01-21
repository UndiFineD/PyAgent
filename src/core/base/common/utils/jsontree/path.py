from __future__ import annotations
import re
from typing import Any
from src.core.base.common.utils.jsontree.types import JSONTree, _T, _U

def _parse_path(path: str, separator: str = ".") -> list[str | int]:
    """Parse a dot-notation path into parts, handling array indices."""
    parts: list[str | int] = []
    
    # Split by separator, but keep array indices
    for part in re.split(rf'(?<!\[){re.escape(separator)}', path):
        # Check for array indices
        match = re.match(r'^(.+?)\[(\d+)\]$', part)
        if match:
            parts.append(match.group(1))
            parts.append(int(match.group(2)))
        elif re.match(r'^\[(\d+)\]$', part):
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
