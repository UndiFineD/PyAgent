# Class Breakdown: ImmutableCollections

**File**: `src\core\base\structures\ImmutableCollections.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ConstantList`

**Line**: 28  
**Inherits**: Unknown, Unknown  
**Methods**: 32

Immutable list wrapper that raises TypeError on mutation attempts.

Wraps an existing list and provides read-only access while maintaining
full Sequence protocol compatibility.

Example:
    >>> data ...

[TIP] **Suggested split**: Move to `constantlist.py`

---

### 2. `ConstantDict`

**Line**: 157  
**Inherits**: Unknown, Unknown  
**Methods**: 22

Immutable dictionary wrapper that raises TypeError on mutation attempts.

Example:
    >>> data = {"a": 1, "b": 2}
    >>> const = ConstantDict(data)
    >>> print(const["a"])  # 1
    >>> const["c"] ...

[TIP] **Suggested split**: Move to `constantdict.py`

---

### 3. `FrozenDict`

**Line**: 250  
**Inherits**: Unknown, Unknown, Hashable  
**Methods**: 16

Immutable and hashable dictionary.

Unlike ConstantDict, FrozenDict creates a copy and is hashable,
making it suitable for use as dictionary keys or set members.

Example:
    >>> fd = FrozenDict({"a"...

[TIP] **Suggested split**: Move to `frozendict.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
