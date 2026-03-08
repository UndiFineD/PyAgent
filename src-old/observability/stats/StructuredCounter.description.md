# StructuredCounter

**File**: `src\observability\stats\StructuredCounter.py`  
**Type**: Python Module  
**Summary**: 6 classes, 2 functions, 9 imports  
**Lines**: 207  
**Complexity**: 11 (moderate)

## Overview

StructuredCounter - Dataclass-based structured metric counters.

Inspired by vLLM's CompilationCounter pattern for tracking detailed metrics
with snapshot/diff capabilities and testing support.

Phase 24: Advanced Observability & Parsing

## Classes (6)

### `StructuredCounter`

Base class for structured metric counters.

Provides snapshot, diff, and testing utilities for tracking
detailed metrics across operations.

Usage:
    @dataclass
    class MyCounter(StructuredCounter):
        requests_processed: int = 0
        cache_hits: int = 0
        cache_misses: int = 0
    
    counter = MyCounter()
    counter.requests_processed += 1
    
    # Test expected changes
    with counter.expect(requests_processed=1, cache_hits=1):
        counter.requests_processed += 1
        counter.cache_hits += 1

**Methods** (7):
- `clone(self)`
- `reset(self)`
- `diff(self, other)`
- `as_dict(self)`
- `expect(self)`
- `increment(self, field_name, amount)`
- `decrement(self, field_name, amount)`

### `CompilationCounter`

**Inherits from**: StructuredCounter

Counter for tracking compilation-related metrics.

Based on vLLM's compilation counter pattern.

### `RequestCounter`

**Inherits from**: StructuredCounter

Counter for tracking request-related metrics.

### `CacheCounter`

**Inherits from**: StructuredCounter

Counter for tracking cache-related metrics.

**Methods** (1):
- `hit_ratio(self)`

### `PoolCounter`

**Inherits from**: StructuredCounter

Counter for tracking object pool metrics.

**Methods** (1):
- `active_objects(self)`

### `QueueCounter`

**Inherits from**: StructuredCounter

Counter for tracking queue metrics.

## Functions (2)

### `get_all_counters()`

Get all global counters.

### `reset_all_counters()`

Reset all global counters.

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `contextlib.contextmanager`
- `copy`
- `dataclasses.dataclass`
- `dataclasses.field`
- `dataclasses.fields`
- `typing.Any`
- `typing.Generator`
- `typing.TypeVar`

---
*Auto-generated documentation*
