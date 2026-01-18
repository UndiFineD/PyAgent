"""
JSONTreeUtils - Nested JSON traversal and transformation utilities.

Phase 22 implementation based on vLLM's jsontree.py patterns.
Provides efficient utilities for working with arbitrarily nested JSON structures.

Features:
- json_iter_leaves: Iterate all leaf values
- json_map_leaves: Apply function to all leaves (structure-preserving)
- json_reduce_leaves: Reduce all leaves to single value
- json_count_leaves: Count leaves in nested structure
- json_flatten: Flatten nested JSON with dot-notation keys
- json_unflatten: Reconstruct nested JSON from flat dict
- json_get_path: Get value at dot-notation path
- json_set_path: Set value at dot-notation path

Performance: Rust-accelerated for common operations.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterable
from functools import reduce
from typing import Any, TypeAlias, TypeVar, overload

logger = logging.getLogger(__name__)

_T = TypeVar("_T")
_U = TypeVar("_U")

# Type alias for nested JSON structures where leaves can be any type
JSONTree: TypeAlias = (
    dict[str, "JSONTree[_T]"] | list["JSONTree[_T]"] | tuple["JSONTree[_T]", ...] | _T
)

# Extended type alias for overload compatibility
_JSONTree: TypeAlias = (
    dict[str, "JSONTree[_T]"]
    | list["JSONTree[_T]"]
    | tuple["JSONTree[_T]", ...]
    | dict[str, _T]
    | list[_T]
    | tuple[_T, ...]
    | _T
)


# ============================================================================
# Leaf Iteration
# ============================================================================


def json_iter_leaves(value: JSONTree[_T]) -> Iterable[_T]:
    """
    Iterate through each leaf in a nested JSON structure.
    
    A leaf is any value that is not a dict, list, or tuple.
    
    Args:
        value: A nested JSON structure (dict, list, tuple, or leaf value).
        
    Yields:
        Each leaf value in depth-first order.
        
    Examples:
        >>> list(json_iter_leaves({"a": 1, "b": {"c": 2}}))
        [1, 2]
        >>> list(json_iter_leaves([1, [2, 3], 4]))
        [1, 2, 3, 4]
        >>> list(json_iter_leaves("leaf"))
        ["leaf"]
    """
    if isinstance(value, dict):
        for v in value.values():
            yield from json_iter_leaves(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from json_iter_leaves(v)
    else:
        yield value


def json_iter_leaves_with_path(
    value: JSONTree[_T], 
    prefix: str = ""
) -> Iterable[tuple[str, _T]]:
    """
    Iterate through each leaf with its dot-notation path.
    
    Args:
        value: A nested JSON structure.
        prefix: Optional path prefix (used for recursion).
        
    Yields:
        Tuples of (path, leaf_value).
        
    Examples:
        >>> list(json_iter_leaves_with_path({"a": {"b": 1}}))
        [("a.b", 1)]
        >>> list(json_iter_leaves_with_path([1, 2]))
        [("[0]", 1), ("[1]", 2)]
    """
    if isinstance(value, dict):
        for k, v in value.items():
            new_prefix = f"{prefix}.{k}" if prefix else k
            yield from json_iter_leaves_with_path(v, new_prefix)
    elif isinstance(value, (list, tuple)):
        for i, v in enumerate(value):
            new_prefix = f"{prefix}[{i}]"
            yield from json_iter_leaves_with_path(v, new_prefix)
    else:
        yield (prefix, value)


# ============================================================================
# Leaf Mapping
# ============================================================================


@overload
def json_map_leaves(
    func: Callable[[_T], _U],
    value: _T | dict[str, _T],
) -> _U | dict[str, _U]: ...


@overload
def json_map_leaves(
    func: Callable[[_T], _U],
    value: _T | list[_T],
) -> _U | list[_U]: ...


@overload
def json_map_leaves(
    func: Callable[[_T], _U],
    value: _T | tuple[_T, ...],
) -> _U | tuple[_U, ...]: ...


@overload
def json_map_leaves(
    func: Callable[[_T], _U],
    value: JSONTree[_T],
) -> JSONTree[_U]: ...


def json_map_leaves(
    func: Callable[[_T], _U],
    value: Any,
) -> _JSONTree[_U]:
    """
    Apply a function to each leaf in a nested JSON structure.
    
    Preserves the structure of the input, replacing each leaf with
    the result of applying func to it.
    
    Args:
        func: Function to apply to each leaf value.
        value: A nested JSON structure.
        
    Returns:
        A new structure with the same shape, but with transformed leaves.
        
    Examples:
        >>> json_map_leaves(lambda x: x * 2, {"a": 1, "b": 2})
        {"a": 2, "b": 4}
        >>> json_map_leaves(str.upper, ["a", ["b", "c"]])
        ["A", ["B", "C"]]
    """
    if isinstance(value, dict):
        return {k: json_map_leaves(func, v) for k, v in value.items()}  # type: ignore
    elif isinstance(value, list):
        return [json_map_leaves(func, v) for v in value]  # type: ignore
    elif isinstance(value, tuple):
        return tuple(json_map_leaves(func, v) for v in value)
    else:
        return func(value)


def json_map_leaves_async(
    func: Callable[[_T], _U],
    value: Any,
) -> _JSONTree[_U]:
    """
    Apply a function to each leaf (async-ready version).
    
    Same as json_map_leaves but can be used with async functions
    when combined with asyncio.gather.
    
    Args:
        func: Function to apply to each leaf value.
        value: A nested JSON structure.
        
    Returns:
        A new structure with transformed leaves.
    """
    return json_map_leaves(func, value)


# ============================================================================
# Leaf Reduction
# ============================================================================


@overload
def json_reduce_leaves(
    func: Callable[[_T, _T], _T],
    value: _T | dict[str, _T],
    /,
) -> _T: ...


@overload
def json_reduce_leaves(
    func: Callable[[_T, _T], _T],
    value: _T | list[_T],
    /,
) -> _T: ...


@overload
def json_reduce_leaves(
    func: Callable[[_T, _T], _T],
    value: _T | tuple[_T, ...],
    /,
) -> _T: ...


@overload
def json_reduce_leaves(
    func: Callable[[_T, _T], _T],
    value: JSONTree[_T],
    /,
) -> _T: ...


@overload
def json_reduce_leaves(
    func: Callable[[_U, _T], _U],
    value: JSONTree[_T],
    initial: _U,
    /,
) -> _U: ...


def json_reduce_leaves(
    func: Callable[[_T, _T], _T] | Callable[[_U, _T], _U],
    value: _JSONTree[_T],
    initial: _U = ...,  # type: ignore[assignment]
    /,
) -> _T | _U:
    """
    Apply a function of two arguments cumulatively to each leaf.
    
    Reduces all leaves to a single value, from left to right.
    
    Args:
        func: A binary function (accumulator, leaf) -> result.
        value: A nested JSON structure.
        initial: Optional initial value for the reduction.
        
    Returns:
        The reduced value.
        
    Examples:
        >>> json_reduce_leaves(lambda a, b: a + b, {"x": 1, "y": 2})
        3
        >>> json_reduce_leaves(lambda a, b: a + b, [1, 2, 3], 10)
        16
    """
    if initial is ...:
        return reduce(func, json_iter_leaves(value))  # type: ignore

    return reduce(func, json_iter_leaves(value), initial)  # type: ignore


# ============================================================================
# Leaf Counting
# ============================================================================


def json_count_leaves(value: JSONTree[_T]) -> int:
    """
    Count the number of leaves in a nested JSON structure.
    
    Args:
        value: A nested JSON structure.
        
    Returns:
        The number of leaf values.
        
    Examples:
        >>> json_count_leaves({"a": 1, "b": {"c": 2, "d": 3}})
        3
        >>> json_count_leaves([1, [2, 3], [[4]]])
        4
    """
    return sum(1 for _ in json_iter_leaves(value))


def json_depth(value: JSONTree[_T]) -> int:
    """
    Calculate the maximum depth of a nested JSON structure.
    
    Args:
        value: A nested JSON structure.
        
    Returns:
        The maximum nesting depth (1 for flat, 0 for leaf).
        
    Examples:
        >>> json_depth({"a": 1})
        1
        >>> json_depth({"a": {"b": {"c": 1}}})
        3
        >>> json_depth("leaf")
        0
    """
    if isinstance(value, dict):
        if not value:
            return 1
        return 1 + max(json_depth(v) for v in value.values())
    elif isinstance(value, (list, tuple)):
        if not value:
            return 1
        return 1 + max(json_depth(v) for v in value)
    else:
        return 0


# ============================================================================
# Flattening and Unflattening
# ============================================================================


def json_flatten(
    value: JSONTree[_T],
    separator: str = ".",
    list_separator: str = "",
) -> dict[str, _T]:
    """
    Flatten a nested JSON structure to a single-level dict with dot-notation keys.
    
    Args:
        value: A nested JSON structure.
        separator: Separator for nested dict keys (default: ".").
        list_separator: Separator for list indices (default: "" for [0] notation).
        
    Returns:
        A flat dict mapping paths to leaf values.
        
    Examples:
        >>> json_flatten({"a": {"b": 1, "c": 2}})
        {"a.b": 1, "a.c": 2}
        >>> json_flatten({"a": [1, 2]})
        {"a[0]": 1, "a[1]": 2}
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
    
    Args:
        flat: A flat dict with dot-notation keys.
        separator: Separator used in keys (default: ".").
        
    Returns:
        A nested dict structure.
        
    Examples:
        >>> json_unflatten({"a.b": 1, "a.c": 2})
        {"a": {"b": 1, "c": 2}}
        >>> json_unflatten({"a[0]": 1, "a[1]": 2})
        {"a": [1, 2]}
    """
    import re
    
    result: dict[str, Any] = {}
    
    for key, value in flat.items():
        parts = _parse_path(key, separator)
        current = result
        
        for i, part in enumerate(parts[:-1]):
            next_part = parts[i + 1]
            
            if isinstance(part, int):
                # Extend list if needed
                while len(current) <= part:
                    current.append(None)
                if current[part] is None:
                    current[part] = [] if isinstance(next_part, int) else {}
                current = current[part]
            else:
                if part not in current:
                    current[part] = [] if isinstance(next_part, int) else {}
                current = current[part]
        
        # Set the final value
        final_part = parts[-1]
        if isinstance(final_part, int):
            while len(current) <= final_part:
                current.append(None)
            current[final_part] = value
        else:
            current[final_part] = value
    
    return result


def _parse_path(path: str, separator: str = ".") -> list[str | int]:
    """Parse a dot-notation path into parts, handling array indices."""
    import re
    
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


# ============================================================================
# Path-based Access
# ============================================================================


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
        
    Examples:
        >>> json_get_path({"a": {"b": 1}}, "a.b")
        1
        >>> json_get_path({"a": [1, 2]}, "a[1]")
        2
        >>> json_get_path({"a": 1}, "b.c", "default")
        "default"
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
        
    Examples:
        >>> d = {"a": {}}
        >>> json_set_path(d, "a.b.c", 1)
        {"a": {"b": {"c": 1}}}
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


# ============================================================================
# Filtering
# ============================================================================


def json_filter_leaves(
    predicate: Callable[[_T], bool],
    value: JSONTree[_T],
) -> JSONTree[_T]:
    """
    Filter leaves in a nested structure, keeping only those matching predicate.
    
    Note: Empty containers are removed from the result.
    
    Args:
        predicate: Function to test each leaf.
        value: A nested JSON structure.
        
    Returns:
        A new structure with only matching leaves.
        
    Examples:
        >>> json_filter_leaves(lambda x: x > 1, {"a": 1, "b": 2, "c": 3})
        {"b": 2, "c": 3}
    """
    if isinstance(value, dict):
        result = {}
        for k, v in value.items():
            filtered = json_filter_leaves(predicate, v)
            # Only include non-empty containers or matching leaves
            if isinstance(filtered, dict) and not filtered:
                continue
            if isinstance(filtered, (list, tuple)) and not filtered:
                continue
            result[k] = filtered
        return result
    elif isinstance(value, list):
        result_list = []
        for v in value:
            filtered = json_filter_leaves(predicate, v)
            if isinstance(filtered, dict) and not filtered:
                continue
            if isinstance(filtered, (list, tuple)) and not filtered:
                continue
            result_list.append(filtered)
        return result_list
    elif isinstance(value, tuple):
        result_tuple = []
        for v in value:
            filtered = json_filter_leaves(predicate, v)
            if isinstance(filtered, dict) and not filtered:
                continue
            if isinstance(filtered, (list, tuple)) and not filtered:
                continue
            result_tuple.append(filtered)
        return tuple(result_tuple)
    else:
        return value if predicate(value) else {}  # type: ignore


# ============================================================================
# Validation
# ============================================================================


def json_validate_leaves(
    validator: Callable[[_T], bool],
    value: JSONTree[_T],
) -> bool:
    """
    Check if all leaves in a structure satisfy a predicate.
    
    Args:
        validator: Function to validate each leaf.
        value: A nested JSON structure.
        
    Returns:
        True if all leaves pass validation, False otherwise.
        
    Examples:
        >>> json_validate_leaves(lambda x: isinstance(x, int), {"a": 1, "b": 2})
        True
        >>> json_validate_leaves(lambda x: x > 0, {"a": 1, "b": -1})
        False
    """
    return all(validator(leaf) for leaf in json_iter_leaves(value))


def json_find_leaves(
    predicate: Callable[[_T], bool],
    value: JSONTree[_T],
) -> list[tuple[str, _T]]:
    """
    Find all leaves matching a predicate, with their paths.
    
    Args:
        predicate: Function to test each leaf.
        value: A nested JSON structure.
        
    Returns:
        List of (path, value) tuples for matching leaves.
        
    Examples:
        >>> json_find_leaves(lambda x: x > 1, {"a": 1, "b": 2, "c": 3})
        [("b", 2), ("c", 3)]
    """
    return [
        (path, leaf) 
        for path, leaf in json_iter_leaves_with_path(value) 
        if predicate(leaf)
    ]


# ============================================================================
# Rust Acceleration Integration
# ============================================================================

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


# ============================================================================
# Exports
# ============================================================================

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
