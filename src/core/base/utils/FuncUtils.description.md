# FuncUtils

**File**: `src\core\base\utils\FuncUtils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 15 functions, 17 imports  
**Lines**: 607  
**Complexity**: 15 (moderate)

## Overview

Function Utilities Module - Phase 20: Production Infrastructure
================================================================

Helper functions and decorators for working with callables.
Inspired by vLLM's func_utils.py pattern.

Features:
- run_once: Ensure a function runs only once
- deprecate_args: Mark positional arguments as deprecated
- deprecate_kwargs: Mark keyword arguments as deprecated
- supports_kw: Check if a callable supports a keyword argument
- memoize: Thread-safe memoization decorator
- throttle: Limit function call frequency
- debounce: Delay function execution until stable
- retry_on_exception: Retry function on specific exceptions

Author: PyAgent Phase 20

## Functions (15)

### `identity(value)`

Returns the first provided value unchanged.

### `run_once(f)`

Decorator ensuring a function runs only once.

Thread-safe. Subsequent calls are silently ignored.

Example:
    >>> @run_once
    ... def init_system():
    ...     print("Initializing...")
    >>> init_system()  # Prints "Initializing..."
    >>> init_system()  # Does nothing

### `run_once_with_result(f)`

Decorator ensuring a function runs only once, caching the result.

Thread-safe. Subsequent calls return the cached result.

### `deprecate_args(start_index, is_deprecated, additional_message)`

Decorator to deprecate positional arguments starting at an index.

Args:
    start_index: The index from which positional args are deprecated.
    is_deprecated: Whether deprecation is active (can be callable).
    additional_message: Additional message to include in the warning.

Example:
    >>> @deprecate_args(2, additional_message="Use keyword args instead")
    ... def foo(a, b, c=None, d=None):
    ...     pass
    >>> foo(1, 2, 3, 4)  # Warns about c and d being passed positionally

### `deprecate_kwargs()`

Decorator to mark specific keyword arguments as deprecated.

Args:
    *kws: Names of deprecated keyword arguments.
    is_deprecated: Whether deprecation is active (can be callable).
    additional_message: Additional message to include in the warning.

Example:
    >>> @deprecate_kwargs("old_param", additional_message="Use new_param")
    ... def foo(new_param=None, old_param=None):
    ...     pass
    >>> foo(old_param=1)  # Warns about old_param

### `deprecated(reason, replacement, version)`

Mark a function as deprecated.

Args:
    reason: Why the function is deprecated.
    replacement: Suggested replacement function.
    version: Version when it will be removed.

### `supports_kw(callable_obj, kw_name)`

Check if a keyword is a valid kwarg for a callable.

Args:
    callable_obj: The callable to check.
    kw_name: The keyword argument name to check for.
    requires_kw_only: If True, only accept keyword-only parameters.
    allow_var_kwargs: If True, **kwargs accepts any keyword.

Returns:
    True if the callable accepts the keyword argument.

### `get_allowed_kwargs(callable_obj, overrides)`

Filter overrides to only include valid keyword arguments.

Args:
    callable_obj: The callable to check against.
    overrides: Potential keyword arguments.
    requires_kw_only: If True, only keep keyword-only arguments.
    allow_var_kwargs: If True, allow arguments for **kwargs.

Returns:
    Dictionary of valid keyword arguments.

### `memoize(fn)`

Thread-safe memoization decorator.

Caches results based on arguments. Arguments must be hashable.

### `memoize_method(fn)`

Memoization decorator for instance methods.

Stores cache on the instance to avoid memory leaks.

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `collections.abc.Callable`
- `collections.abc.Mapping`
- `functools`
- `functools.lru_cache`
- `functools.partial`
- `functools.wraps`
- `inspect`
- `logging`
- `threading`
- `time`
- `typing.Any`
- `typing.Generic`
- `typing.ParamSpec`
- `typing.TypeVar`
- ... and 2 more

---
*Auto-generated documentation*
