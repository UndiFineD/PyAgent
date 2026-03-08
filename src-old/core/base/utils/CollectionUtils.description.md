# CollectionUtils

**File**: `src\core\base\utils\CollectionUtils.py`  
**Type**: Python Module  
**Summary**: 1 classes, 23 functions, 17 imports  
**Lines**: 570  
**Complexity**: 34 (complex)

## Overview

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

## Classes (1)

### `LazyDict`

**Inherits from**: Unknown, Unknown

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

**Methods** (11):
- `__init__(self, factory)`
- `__getitem__(self, key)`
- `__setitem__(self, key, value)`
- `__delitem__(self, key)`
- `__iter__(self)`
- `__len__(self)`
- `__contains__(self, key)`
- `is_computed(self, key)`
- `clear_cache(self, key)`
- `keys(self)`
- ... and 1 more methods

## Functions (23)

### `as_list(maybe_list)`

Convert an iterable to a list, unless it's already a list.

Avoids unnecessary copying for lists.

### `as_iter(obj)`

Convert a single object or iterable to an iterable.

Strings are treated as single objects, not iterables.

### `is_list_of(value, typ)`

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

### `chunk_list(lst, chunk_size)`

Yield successive chunks of a specified size from a list.

Example:
    >>> list(chunk_list([1, 2, 3, 4, 5], 2))
    [[1, 2], [3, 4], [5]]

### `chunk_iter(iterable, chunk_size)`

Yield successive chunks of a specified size from any iterable.

More memory efficient than chunk_list for large iterables.

### `flatten_2d_lists(lists)`

Flatten a list of lists to a single list.

Example:
    >>> flatten_2d_lists([[1, 2], [3, 4], [5]])
    [1, 2, 3, 4, 5]

### `flatten_deep(nested, max_depth)`

Recursively flatten a deeply nested structure.

Args:
    nested: The nested structure to flatten.
    max_depth: Maximum recursion depth (-1 for unlimited).

Example:
    >>> flatten_deep([[1, [2, 3]], [4, [5, [6]]]])
    [1, 2, 3, 4, 5, 6]

### `full_groupby(values)`

Group items by key, without requiring sorted input.

Unlike itertools.groupby, groups are not broken by non-contiguous data.

Example:
    >>> list(full_groupby([1, 2, 3, 1, 2], key=lambda x: x % 2))
    [(1, [1, 3, 1]), (0, [2, 2])]

### `partition(values, predicate)`

Partition items into two lists based on a predicate.

Returns:
    Tuple of (matching, non_matching) lists.

Example:
    >>> partition([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
    ([2, 4], [1, 3, 5])

### `first(iterable, default)`

Return the first item from an iterable, or default if empty.

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `collections.abc.Callable`
- `collections.abc.Generator`
- `collections.abc.Hashable`
- `collections.abc.Iterable`
- `collections.abc.Iterator`
- `collections.abc.Mapping`
- `collections.abc.MutableMapping`
- `collections.abc.Sequence`
- `collections.defaultdict`
- `itertools`
- `typing.Any`
- `typing.Generic`
- `typing.Literal`
- `typing.TypeVar`
- ... and 2 more

---
*Auto-generated documentation*
