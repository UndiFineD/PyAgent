from __future__ import annotations
from typing import Callable, overload
from functools import reduce
from src.core.base.common.utils.jsontree.types import JSONTree, _JSONTree, _T, _U
from src.core.base.common.utils.jsontree.iteration import json_iter_leaves

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
    """
    if initial is ...:
        return reduce(func, json_iter_leaves(value))  # type: ignore

    return reduce(func, json_iter_leaves(value), initial)  # type: ignore
