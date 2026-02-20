#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Mapping.py module.
"""


from __future__ import annotations

from typing import Any, Callable, overload

try:
    from .types import _T, _U, JSONTree, _JSONTree
except Exception:
    from src.core.base.common.utils.jsontree.types import _T, _U, JSONTree, _JSONTree


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
    """Apply a function to each leaf in a nested JSON structure.

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
    if isinstance(value, list):
        return [json_map_leaves(func, v) for v in value]  # type: ignore
    if isinstance(value, tuple):
        return tuple(json_map_leaves(func, v) for v in value)

    return func(value)


def json_map_leaves_async(
    func: Callable[[_T], _U],
    value: Any,
) -> _JSONTree[_U]:
    """Apply a function to each leaf (async-ready version).

    Same as json_map_leaves but can be used with async functions
    when combined with asyncio.gather.

    Args:
        func: Function to apply to each leaf value.
        value: A nested JSON structure.

    Returns:
        A new structure with transformed leaves.
    """
    return json_map_leaves(func, value)
