from __future__ import annotations
from typing import Any
from src.core.base.common.utils.jsontree.types import JSONTree, _T
from src.core.base.common.utils.jsontree.path import _parse_path

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
