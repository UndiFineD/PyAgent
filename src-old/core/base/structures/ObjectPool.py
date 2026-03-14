r"""LLM_CONTEXT_START

## Source: src-old/core/base/structures/ObjectPool.description.md

# ObjectPool

**File**: `src\\core\base\\structures\\ObjectPool.py`  
**Type**: Python Module  
**Summary**: 7 classes, 6 functions, 17 imports  
**Lines**: 542  
**Complexity**: 40 (complex)

## Overview

Object Pool for reducing GC pressure.

Phase 19: Beyond vLLM - Performance Patterns
Reusable object pooling to minimize allocations.

## Classes (7)

### `Resettable`

**Inherits from**: Protocol

Protocol for objects that can be reset for reuse.

**Methods** (1):
- `reset(self)`

### `PoolStats`

Statistics for object pool.

**Methods** (3):
- `reuse_ratio(self)`
- `total_acquisitions(self)`
- `to_dict(self)`

### `ObjectPool`

**Inherits from**: Unknown

Generic object pool for reducing allocation overhead.

Features:
- Configurable min/max pool size
- Factory function for creating new objects
- Optional reset function for object reuse
- Thread-safe operations
- Statistics tracking
- Context manager support

Example:
    pool = ObjectPool(
        factory=lambda: BytesIO(),
        reset=lambda obj: obj.seek(0) or obj.truncate(),
        max_size=100,
    )
    
    with pool.acquire() as buffer:
        buffer.write(b"data")

**Methods** (10):
- `__init__(self, factory, reset, validator, min_size, max_size, max_idle_seconds)`
- `_warm_pool(self)`
- `acquire(self)`
- `release(self, obj)`
- `borrow(self)`
- `clear(self)`
- `prune(self, max_age_seconds)`
- `size(self)`
- `stats(self)`
- `__len__(self)`

### `TypedObjectPool`

**Inherits from**: Unknown

Object pool that works with Resettable objects.

Automatically calls reset() on objects that implement the protocol.

**Methods** (5):
- `__init__(self, factory, max_size)`
- `acquire(self)`
- `release(self, obj)`
- `borrow(self)`
- `stats(self)`

### `BufferPool`

Specialized pool for byte buffers.

Pre-allocates buffers of specific sizes for zero-copy operations.

**Methods** (6):
- `__init__(self, buffer_size, max_buffers)`
- `acquire(self)`
- `release(self, buffer)`
- `borrow(self)`
- `buffer_size(self)`
- `stats(self)`

### `TieredBufferPool`

Multi-tier buffer pool with different size classes.

Automatically selects the smallest buffer that fits the request.

**Methods** (6):
- `__init__(self, sizes, max_buffers_per_tier)`
- `_find_tier(self, size)`
- `acquire(self, size)`
- `release(self, buffer)`
- `borrow(self, size)`
- `get_stats(self)`

### `PooledContextManager`

**Inherits from**: Unknown

Wrapper that makes any pooled object a context manager.

**Methods** (3):
- `__init__(self, pool, obj)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`

## Functions (6)

### `get_list_pool(max_size)`

Get global list pool.

### `get_dict_pool(max_size)`

Get global dict pool.

### `get_set_pool(max_size)`

Get global set pool.

### `pooled_list()`

Get a pooled list that's automatically returned.

### `pooled_dict()`

Get a pooled dict that's automatically returned.

### `pooled_set()`

Get a pooled set that's automatically returned.

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `collections.deque`
- `contextlib.contextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Generic`
- `typing.List`
- `typing.Optional`
- `typing.Protocol`
- `typing.TypeVar`
- ... and 2 more

---
*Auto-generated documentation*
## Source: src-old/core/base/structures/ObjectPool.improvements.md

# Improvements for ObjectPool

**File**: `src\\core\base\\structures\\ObjectPool.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 542 lines (large)  
**Complexity**: 40 score (complex)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ObjectPool_test.py` with pytest tests

### Code Organization
- [TIP] **7 classes in one file** - Consider splitting into separate modules

### File Complexity
- [!] **Large file** (542 lines) - Consider refactoring

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END

"""
