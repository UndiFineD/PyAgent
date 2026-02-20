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


"""JSON Tree Meta Utilities.

Helper utilities for analyzing and transforming nested JSON-like trees used
across the codebase. Functions include counting leaves, computing depth,
filtering leaves by predicate, and validating leaf values.
"""


from __future__ import annotations

"""JSON Tree Meta Utilities.

Helper utilities for analyzing and transforming nested JSON-like trees used
across the codebase. Functions include counting leaves, computing depth,
filtering leaves by predicate, and validating leaf values.
"""

from typing import Callable, Any, TypeVar

from .iteration import json_iter_leaves, json_iter_leaves_with_path
from .types import _T, JSONTree


def json_count_leaves(value: JSONTree[_T]) -> int:
    """Count the number of leaves in a nested JSON structure."""
    return sum(1 for _ in json_iter_leaves(value))


def json_depth(value: JSONTree[_T]) -> int:
    """Calculate the maximum depth of a nested JSON structure."""
    if isinstance(value, dict):
        if not value:
            return 1
        return 1 + max(json_depth(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        if not value:
            return 1
        return 1 + max(json_depth(v) for v in value)

    return 0


def json_filter_leaves(
    predicate: Callable[[_T], bool],
    value: JSONTree[_T],
) -> JSONTree[_T]:
    """Filter leaves in a nested structure, keeping only those matching predicate."""
    if isinstance(value, dict):
        result = {}
        for k, v in value.items():
            filtered = json_filter_leaves(predicate, v)
            if isinstance(filtered, dict) and not filtered:
                continue
            if isinstance(filtered, (list, tuple)) and not filtered:
                continue
            result[k] = filtered
        return result
    if isinstance(value, list):
        result_list = []
        for v in value:
            filtered = json_filter_leaves(predicate, v)
            if isinstance(filtered, dict) and not filtered:
                continue
            if isinstance(filtered, (list, tuple)) and not filtered:
                continue
            result_list.append(filtered)
        return result_list
    if isinstance(value, tuple):
        result_tuple = []
        for v in value:
            filtered = json_filter_leaves(predicate, v)
            if isinstance(filtered, dict) and not filtered:
                continue
            if isinstance(filtered, (list, tuple)) and not filtered:
                continue
            result_tuple.append(filtered)
        return tuple(result_tuple)

    return value if predicate(value) else {}  # type: ignore


def json_validate_leaves(
    validator: Callable[[_T], bool],
    value: JSONTree[_T],
) -> bool:
    """Check if all leaves in a structure satisfy a predicate."""
    return all(validator(leaf) for leaf in json_iter_leaves(value))


def json_find_leaves(
    predicate: Callable[[_T], bool],
    value: JSONTree[_T],
) -> list[tuple[str, _T]]:
    """Find all leaves matching a predicate, with their paths."""
    return [(path, leaf) for path, leaf in json_iter_leaves_with_path(value) if predicate(leaf)]
