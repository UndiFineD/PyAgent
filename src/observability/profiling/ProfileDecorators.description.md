# ProfileDecorators

**File**: `src\observability\profiling\ProfileDecorators.py`  
**Type**: Python Module  
**Summary**: 2 classes, 7 functions, 15 imports  
**Lines**: 314  
**Complexity**: 15 (moderate)

## Overview

ProfileDecorators - cProfile-based profiling utilities.

Inspired by vLLM's profiling.py patterns for ad-hoc profiling.

Provides decorators and context managers for profiling Python code
with cProfile, integrated with RustProfiler for unified reporting.

Phase 17: vLLM Pattern Integration (P2)

## Classes (2)

### `ProfileResult`

Result from a profiling session.

**Methods** (2):
- `summary(self)`
- `print_stats(self, limit)`

### `ProfileAccumulator`

Accumulates profiling data across multiple calls.

Useful for tracking function performance over time.

Example:
    >>> acc = ProfileAccumulator()
    >>> 
    >>> @acc.track
    ... def my_function():
    ...     pass
    >>> 
    >>> for _ in range(100):
    ...     my_function()
    >>> 
    >>> print(acc.report())

**Methods** (6):
- `__init__(self)`
- `record(self, name, elapsed_seconds)`
- `track(self, func)`
- `report(self)`
- `reset(self)`
- `print_report(self)`

## Functions (7)

### `cprofile_context(enabled, output_file, print_stats, limit)`

Context manager for cProfile profiling.

Args:
    enabled: Whether profiling is enabled
    output_file: Optional file to save stats
    print_stats: Whether to print stats on exit
    limit: Number of top functions to show
    
Yields:
    ProfileResult with timing and stats
    
Example:
    >>> with cprofile_context(print_stats=True) as result:
    ...     expensive_operation()
    >>> print(f"Took {result.elapsed_ms}ms")

### `cprofile(enabled, output_file, print_stats, limit)`

Decorator for cProfile profiling.

Args:
    enabled: Whether profiling is enabled
    output_file: Optional file to save stats
    print_stats: Whether to print stats after call
    limit: Number of top functions to show
    
Returns:
    Decorated function
    
Example:
    >>> @cprofile(print_stats=True)
    ... def slow_function():
    ...     time.sleep(0.1)
    >>> slow_function()

### `timer_context(name)`

Simple timing context manager.

Args:
    name: Name for the timed operation
    
Yields:
    Dict with timing info (populated on exit)
    
Example:
    >>> with timer_context("data_load") as timing:
    ...     data = load_data()
    >>> print(f"Took {timing['elapsed_ms']:.2f}ms")

### `timer(name)`

Simple timing decorator.

Args:
    name: Optional name (defaults to function name)
    
Returns:
    Decorated function that prints timing
    
Example:
    >>> @timer()
    ... def slow_function():
    ...     time.sleep(0.1)

### `track(func)`

Decorator to track function timing in global accumulator.

### `get_profile_report()`

Get report from global accumulator.

### `reset_profile_data()`

Reset global accumulator.

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `cProfile`
- `contextlib.contextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `functools`
- `io`
- `pathlib.Path`
- `pstats`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Iterator`
- `typing.ParamSpec`
- `typing.TypeVar`

---
*Auto-generated documentation*
