#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Collection Utilities Module - Phase 20: Production Infrastructure
==================================================================

Helper functions and classes for working with collections.
Inspired by vLLM's collection_utils.py pattern.

Features:
- LazyDict: Evaluates values only when accessed
- chunk_list: Yield successive chunks from a list
- flatten_2d_lists: Flatten nested lists
- full_groupby: Group items without requiring sorted input
- is_list_of: Type guard for homogeneous lists
- as_list/as_iter: Convert iterables to lists/iterators
- swap_dict_values: Swap values between two dictionary keys
- deep_merge_dicts: Recursively merge dictionaries
- invert_dict: Invert a dictionary (swap keys and values)
- filter_none: Filter None values from collections

Author: PyAgent Phase 20
"""

from __future__ import annotations

import itertools
from collections import defaultdict
from collections.abc import (Callable, Generator, Hashable, Iterable, Iterator,
                             Mapping)
from typing import Any, Generic, Literal, TypeVar

from typing_extensions import TypeIs

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


# ============================================================================
# LazyDict
# ============================================================================


class LazyDict(Mapping[str, V], Generic[V]):
    """
    Evaluates dictionary items only when they are accessed.

    Useful for expensive computations that should only run when needed.

    Example:
        >>> def expensive_compute():
        ...     print("Computing...")
        ...     return 42
        >>> d = LazyDict({"value": expensive_compute})
        >>> # No output yet - not computed
        >>> print(d["value"])  # Now computes
        Computing...
        42
        >>> print(d["value"])  # Uses cached value
        42
    """

    __slots__ = ("_factory", "_cache")

    def __init__(self, factory: dict[str, Callable[[], V]]) -> None:
        """
        Initialize a lazy dictionary.

        Args:
            factory: Dictionary mapping keys to factory functions.
        """
        self._factory = dict(factory)
        self._cache: dict[str, V] = {}

    def __getitem__(self, key: str) -> V:
        if key not in self._cache:
            if key not in self._factory:
                raise KeyError(key)
            self._cache[key] = self._factory[key]()
        return self._cache[key]

    def __setitem__(self, key: str, value: Callable[[], V]) -> None:
        """Set a new factory function for a key (clears cache)."""
        self._factory[key] = value
        self._cache.pop(key, None)  # Clear cached value if any

    def __delitem__(self, key: str) -> None:
        """Delete a key from the factory and cache."""
        if key in self._factory:
            del self._factory[key]
        self._cache.pop(key, None)

    def __iter__(self) -> Iterator[str]:
        return iter(self._factory)

    def __len__(self) -> int:
        return len(self._factory)

    def __contains__(self, key: object) -> bool:
        return key in self._factory

    def is_computed(self, key: str) -> bool:
        """Check if a value has been computed and cached."""
        return key in self._cache

    def clear_cache(self, key: str | None = None) -> None:
        """
        Clear cached computed values.

        Args:
            key: If provided, clear only this key. Otherwise clear all.
        """
        if key is None:
            self._cache.clear()
        else:
            self._cache.pop(key, None)

    def keys(self) -> Iterable[str]:
        return self._factory.keys()

    def computed_keys(self) -> Iterable[str]:
        """Return keys that have been computed."""
        return self._cache.keys()


# ============================================================================
# List Utilities
# ============================================================================


def as_list(maybe_list: Iterable[T]) -> list[T]:
    """
    Convert an iterable to a list, unless it's already a list.

    Avoids unnecessary copying for lists.
    """
    return maybe_list if isinstance(maybe_list, list) else list(maybe_list)


def as_iter(obj: T | Iterable[T]) -> Iterable[T]:
    """
    Convert a single object or iterable to an iterable.

    Strings are treated as single objects, not iterables.
    """
    if isinstance(obj, str) or not isinstance(obj, Iterable):
        return [obj]  # type: ignore[list-item]
    return obj


def is_list_of(
    value: object,
    typ: type[T] | tuple[type[T], ...],
    *,
    check: Literal["first", "all"] = "first",
) -> TypeIs[list[T]]:
    """
    Type guard to check if value is a list of a specific type.

    Args:
        value: The value to check.
        typ: The expected element type(s).
        check: "first" checks only the first element (fast),
               "all" checks every element (thorough).

    Returns:
        True if value is a list of the specified type.

    Example:
        >>> is_list_of([1, 2, 3], int)
        True
        >>> is_list_of(["a", "b"], int)
        False
    """
    if not isinstance(value, list):
        return False

    if not value:  # Empty list
        return True

    if check == "first":
        return isinstance(value[0], typ)
    if check == "all":
        return all(isinstance(v, typ) for v in value)

    raise ValueError(f"Invalid check mode: {check}")


def chunk_list(lst: list[T], chunk_size: int) -> Generator[list[T], None, None]:
    """
    Yield successive chunks of a specified size from a list.

    Example:
        >>> list(chunk_list([1, 2, 3, 4, 5], 2))
        [[1, 2], [3, 4], [5]]
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


def chunk_iter(iterable: Iterable[T], chunk_size: int) -> Generator[list[T], None, None]:
    """
    Yield successive chunks of a specified size from any iterable.

    More memory efficient than chunk_list for large iterables.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    iterator = iter(iterable)
    while True:
        chunk = list(itertools.islice(iterator, chunk_size))
        if not chunk:
            break
        yield chunk


def flatten_2d_lists(lists: Iterable[Iterable[T]]) -> list[T]:
    """
    Flatten a list of lists to a single list.

    Example:
        >>> flatten_2d_lists([[1, 2], [3, 4], [5]])
        [1, 2, 3, 4, 5]
    """
    return [item for sublist in lists for item in sublist]


def flatten_deep(nested: Any, max_depth: int = -1) -> list[Any]:
    """
    Recursively flatten a deeply nested structure.

    Args:
        nested: The nested structure to flatten.
        max_depth: Maximum recursion depth (-1 for unlimited).

    Example:
        >>> flatten_deep([[1, [2, 3]], [4, [5, [6]]]])
        [1, 2, 3, 4, 5, 6]
    """
    result: list[Any] = []

    def _flatten(item: Any, depth: int) -> None:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, Iterable) and (max_depth == -1 or depth < max_depth):
            for subitem in item:
                _flatten(subitem, depth + 1)
        else:
            result.append(item)

    _flatten(nested, 0)
    return result


# ============================================================================
# Grouping Utilities
# ============================================================================


def full_groupby(values: Iterable[V], *, key: Callable[[V], K]) -> Iterable[tuple[K, list[V]]]:
    """
    Group items by key, without requiring sorted input.

    Unlike itertools.groupby, groups are not broken by non-contiguous data.

    Example:
        >>> list(full_groupby([1, 2, 3, 1, 2], key=lambda x: x % 2))
        [(1, [1, 3, 1]), (0, [2, 2])]
    """
    groups: dict[K, list[V]] = defaultdict(list)

    for value in values:
        groups[key(value)].append(value)

    return groups.items()


def partition(values: Iterable[T], predicate: Callable[[T], bool]) -> tuple[list[T], list[T]]:
    """
    Partition items into two lists based on a predicate.

    Returns:
        Tuple of (matching, non_matching) lists.

    Example:
        >>> partition([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
        ([2, 4], [1, 3, 5])
    """
    matching: list[T] = []
    non_matching: list[T] = []

    for value in values:
        if predicate(value):
            matching.append(value)
        else:
            non_matching.append(value)

    return matching, non_matching


def first(iterable: Iterable[T], default: T | None = None) -> T | None:
    """
    Return the first item from an iterable, or default if empty.
    """
    return next(iter(iterable), default)


def first_or_raise(iterable: Iterable[T]) -> T:
    """
    Return the first item from an iterable, or raise StopIteration.
    """
    return next(iter(iterable))


def last(iterable: Iterable[T], default: T | None = None) -> T | None:
    """
    Return the last item from an iterable, or default if empty.
    """
    item = default
    for item in iterable:
        pass
    return item


# ============================================================================
# Dictionary Utilities
# ============================================================================


def swap_dict_values(obj: dict[K, V], key1: K, key2: K) -> None:
    """
    Swap values between two dictionary keys in place.

    Handles missing keys gracefully.
    """
    v1 = obj.get(key1)
    v2 = obj.get(key2)

    if v1 is not None:
        obj[key2] = v1
    else:
        obj.pop(key2, None)

    if v2 is not None:
        obj[key1] = v2
    else:
        obj.pop(key1, None)


def deep_merge_dicts(base: dict[str, Any], override: dict[str, Any], *, inplace: bool = False) -> dict[str, Any]:
    """
    Recursively merge two dictionaries.

    Args:
        base: The base dictionary.
        override: Dictionary whose values override base.
        inplace: If True, modify base in place.

    Returns:
        Merged dictionary.
    """
    result = base if inplace else dict(base)

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


def invert_dict(d: dict[K, V]) -> dict[V, K]:
    """
    Invert a dictionary, swapping keys and values.

    Note: Values must be hashable. Duplicate values will be overwritten.
    """
    return {v: k for k, v in d.items()}


def invert_dict_multi(d: dict[K, V]) -> dict[V, list[K]]:
    """
    Invert a dictionary, collecting all keys with the same value.

    Example:
        >>> invert_dict_multi({"a": 1, "b": 1, "c": 2})
        {1: ["a", "b"], 2: ["c"]}
    """
    result: dict[V, list[K]] = defaultdict(list)
    for key, value in d.items():
        result[value].append(key)
    return dict(result)


def filter_none(d: dict[K, V | None]) -> dict[K, V]:
    """
    Return a new dictionary with None values filtered out.
    """
    return {k: v for k, v in d.items() if v is not None}


def pick_keys(d: dict[K, V], keys: Iterable[K]) -> dict[K, V]:
    """
    Return a new dictionary with only the specified keys.
    """
    key_set = set(keys)
    return {k: v for k, v in d.items() if k in key_set}


def omit_keys(d: dict[K, V], keys: Iterable[K]) -> dict[K, V]:
    """
    Return a new dictionary without the specified keys.
    """
    key_set = set(keys)
    return {k: v for k, v in d.items() if k not in key_set}


# ============================================================================
# Unique Utilities
# ============================================================================


def unique(iterable: Iterable[T]) -> list[T]:
    """
    Return unique items preserving order.

    Items must be hashable.
    """
    seen: set[T] = set()
    result: list[T] = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def unique_by(iterable: Iterable[T], key: Callable[[T], Hashable]) -> list[T]:
    """
    Return unique items by key, preserving order.

    Example:
        >>> unique_by([{"id": 1}, {"id": 2}, {"id": 1}], key=lambda x: x["id"])
        [{"id": 1}, {"id": 2}]
    """
    seen: set[Hashable] = set()
    result: list[T] = []
    for item in iterable:
        k = key(item)
        if k not in seen:
            seen.add(k)
            result.append(item)
    return result


# ============================================================================
# Sliding Window
# ============================================================================


def sliding_window(iterable: Iterable[T], size: int) -> Generator[tuple[T, ...], None, None]:
    """
    Yield sliding windows of a specified size.

    Example:
        >>> list(sliding_window([1, 2, 3, 4, 5], 3))
        [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    """
    if size <= 0:
        raise ValueError("size must be positive")

    iterator = iter(iterable)
    window = tuple(itertools.islice(iterator, size))

    if len(window) == size:
        yield window

    for item in iterator:
        window = window[1:] + (item,)
        yield window


def pairwise(iterable: Iterable[T]) -> Generator[tuple[T, T], None, None]:
    """
    Yield consecutive pairs from an iterable.

    Example:
        >>> list(pairwise([1, 2, 3, 4]))
        [(1, 2), (2, 3), (3, 4)]
    """
    iterator = iter(iterable)
    prev = next(iterator, None)
    if prev is None:
        return
    for item in iterator:
        yield (prev, item)  # type: ignore
        prev = item


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # LazyDict
    "LazyDict",
    # List utilities
    "as_list",
    "as_iter",
    "is_list_of",
    "chunk_list",
    "chunk_iter",
    "flatten_2d_lists",
    "flatten_deep",
    # Grouping
    "full_groupby",
    "partition",
    "first",
    "first_or_raise",
    "last",
    # Dictionary utilities
    "swap_dict_values",
    "deep_merge_dicts",
    "invert_dict",
    "invert_dict_multi",
    "filter_none",
    "pick_keys",
    "omit_keys",
    # Unique
    "unique",
    "unique_by",
    # Sliding window
    "sliding_window",
    "pairwise",
]
