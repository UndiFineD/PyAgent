# Class Breakdown: profile_decorators

**File**: `src\observability\profiling\profile_decorators.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ProfileResult`

**Line**: 43  
**Methods**: 2

Result from a profiling session.

[TIP] **Suggested split**: Move to `profileresult.py`

---

### 2. `ProfileAccumulator`

**Line**: 235  
**Methods**: 6

Accumulates profiling data across multiple calls.

Useful for tracking function performance over time.

Example:
    >>> acc = ProfileAccumulator()
    >>>
    >>> @acc.track
    ... def my_function()...

[TIP] **Suggested split**: Move to `profileaccumulator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
