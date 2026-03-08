# ImmutableCollections

**File**: `src\core\base\structures\ImmutableCollections.py`  
**Type**: Python Module  
**Summary**: 3 classes, 1 functions, 9 imports  
**Lines**: 348  
**Complexity**: 71 (very_complex)

## Overview

ImmutableCollections - Read-only collection wrappers.

Implements vLLM's ConstantList pattern and extends it to dictionaries.
These wrappers prevent accidental mutation while maintaining full
sequence/mapping protocol compatibility.

Phase 23: Advanced Serialization & Validation

## Classes (3)

### `ConstantList`

**Inherits from**: Unknown, Unknown

Immutable list wrapper that raises TypeError on mutation attempts.

Wraps an existing list and provides read-only access while maintaining
full Sequence protocol compatibility.

Example:
    >>> data = [1, 2, 3, 4, 5]
    >>> const = ConstantList(data)
    >>> print(const[0])  # 1
    >>> const.append(6)  # TypeError: Cannot append to a constant list

**Methods** (32):
- `__init__(self, data)`
- `append(self, item)`
- `extend(self, items)`
- `insert(self, index, item)`
- `pop(self, index)`
- `remove(self, item)`
- `clear(self)`
- `reverse(self)`
- `sort(self)`
- `__setitem__(self, index, value)`
- ... and 22 more methods

### `ConstantDict`

**Inherits from**: Unknown, Unknown

Immutable dictionary wrapper that raises TypeError on mutation attempts.

Example:
    >>> data = {"a": 1, "b": 2}
    >>> const = ConstantDict(data)
    >>> print(const["a"])  # 1
    >>> const["c"] = 3  # TypeError: Cannot set item in a constant dict

**Methods** (22):
- `__init__(self, data)`
- `__setitem__(self, key, value)`
- `__delitem__(self, key)`
- `pop(self, key)`
- `popitem(self)`
- `clear(self)`
- `update(self)`
- `setdefault(self, key, default)`
- `__getitem__(self, key)`
- `__len__(self)`
- ... and 12 more methods

### `FrozenDict`

**Inherits from**: Unknown, Unknown, Hashable

Immutable and hashable dictionary.

Unlike ConstantDict, FrozenDict creates a copy and is hashable,
making it suitable for use as dictionary keys or set members.

Example:
    >>> fd = FrozenDict({"a": 1, "b": 2})
    >>> cache = {fd: "cached_value"}
    >>> print(hash(fd))  # Valid hash

**Methods** (16):
- `__init__(self, data)`
- `__getitem__(self, key)`
- `__len__(self)`
- `__iter__(self)`
- `__contains__(self, key)`
- `__hash__(self)`
- `__eq__(self, other)`
- `__repr__(self)`
- `keys(self)`
- `values(self)`
- ... and 6 more methods

## Functions (1)

### `as_constant(obj)`

Wrap a list or dict as immutable.

Args:
    obj: List or dict to wrap
    
Returns:
    ConstantList or ConstantDict wrapper

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `collections.abc.Hashable`
- `collections.abc.Iterator`
- `collections.abc.Mapping`
- `collections.abc.Sequence`
- `typing.Any`
- `typing.Generic`
- `typing.TypeVar`
- `typing.overload`

---
*Auto-generated documentation*
