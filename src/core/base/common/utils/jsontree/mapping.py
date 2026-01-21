from __future__ import annotations
from typing import Any, Callable, overload
from src.core.base.common.utils.jsontree.types import JSONTree, _JSONTree, _T, _U

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
