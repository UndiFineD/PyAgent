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


"""Iteration helpers for JSON-like trees."""

try:
    from __future__ import annotations
except ImportError:
    from __future__ import annotations


try:
    from typing import Generator, Iterable, Tuple, TypeVar, Any
except ImportError:
    from typing import Generator, Iterable, Tuple, TypeVar, Any


_T = TypeVar("_T")
JSONTree = Any


def json_iter_leaves(value: JSONTree) -> Iterable[Any]:
    """Yield each leaf in a nested JSON structure (depth-first)."""
    if isinstance(value, dict):
        for v in value.values():
            yield from json_iter_leaves(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from json_iter_leaves(v)
    else:
        yield value


def json_iter_leaves_with_path(value: JSONTree, prefix: str = "") -> Generator[Tuple[str, Any], None, None]:
    """Yield (path, leaf) pairs. Paths use dot/bracket notation for keys/indexes."""
    if isinstance(value, dict):
        for k, v in value.items():
            new_prefix = f"{prefix}.{k}" if prefix else str(k)
            yield from json_iter_leaves_with_path(v, new_prefix)
    elif isinstance(value, (list, tuple)):
        for i, v in enumerate(value):
            new_prefix = f"{prefix}[{i}]" if prefix else f"[{i}]"
            yield from json_iter_leaves_with_path(v, new_prefix)
    else:
        yield (prefix, value)

