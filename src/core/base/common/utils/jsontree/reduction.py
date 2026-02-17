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


"""Reduction.py module.
"""
from __future__ import annotations

from functools import reduce
from typing import Callable, overload

from src.core.base.common.utils.jsontree.iteration import json_iter_leaves
from src.core.base.common.utils.jsontree.types import (_T, _U, JSONTree,
                                                       _JSONTree)


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
    """Apply a function of two arguments cumulatively to each leaf.

    Reduces all leaves to a single value, from left to right.

    Args:
        func: A binary function (accumulator, leaf) -> result.
        value: A nested JSON structure.
        initial: Optional initial value for the reduction.

    Returns:
        The reduced value.
    """if initial is ...:
        return reduce(func, json_iter_leaves(value))  # type: ignore

    return reduce(func, json_iter_leaves(value), initial)  # type: ignore
