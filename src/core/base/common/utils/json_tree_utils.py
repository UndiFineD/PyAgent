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


"""Small JSON tree utilities used in tests.

This file provides lightweight, dependency-free helpers for traversing and
transforming JSON-like trees (dicts/lists). Implementations are intentionally
minimal to keep test collection robust.
"""

from __future__ import annotations

from typing import Any, Generator, Iterable, List, Tuple

JSONTree = Any


def json_iter_leaves(tree: JSONTree) -> Iterable[Any]:
    """Yield all leaf values in a JSON-like tree."""
    if isinstance(tree, dict):
        for v in tree.values():
            yield from json_iter_leaves(v)
    elif isinstance(tree, list):
        for v in tree:
            yield from json_iter_leaves(v)
    else:
        yield tree


def json_iter_leaves_with_path(tree: JSONTree, path: Tuple = ()) -> Generator[Tuple[Tuple, Any], None, None]:
    """Yield pairs of (path_tuple, leaf_value)."""
    if isinstance(tree, dict):
        for k, v in tree.items():
            yield from json_iter_leaves_with_path(v, path + (k,))
    elif isinstance(tree, list):
        for i, v in enumerate(tree):
            yield from json_iter_leaves_with_path(v, path + (i,))
    else:
        yield path, tree


def json_map_leaves(tree: JSONTree, func) -> JSONTree:
    """Return a new tree with func applied to each leaf."""
    if isinstance(tree, dict):
        return {k: json_map_leaves(v, func) for k, v in tree.items()}
    if isinstance(tree, list):
        return [json_map_leaves(v, func) for v in tree]
    return func(tree)


def json_count_leaves(tree: JSONTree) -> int:
    return sum(1 for _ in json_iter_leaves(tree))


def json_depth(tree: JSONTree) -> int:
    if isinstance(tree, dict):
        return 1 + (max((json_depth(v) for v in tree.values()), default=0))
    if isinstance(tree, list):
        return 1 + (max((json_depth(v) for v in tree), default=0))
    return 0


def json_flatten(tree: JSONTree) -> List[Any]:
    return list(json_iter_leaves(tree))


def json_unflatten(flat: List[Any]) -> List[Any]:
    """Return the flat list unchanged — placeholder for tests that import it."""
    return list(flat)


__all__ = [
    "JSONTree",
    "json_iter_leaves",
    "json_iter_leaves_with_path",
    "json_map_leaves",
    "json_count_leaves",
    "json_depth",
    "json_flatten",
    "json_unflatten",
]
