"""LLM_CONTEXT_START

## Source: src-old/core/base/structures/__init__.description.md

# __init__

**File**: `src\\core\base\\structures\\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 29 imports  
**Lines**: 85  
**Complexity**: 0 (simple)

## Overview

Base data structures.

Phase 18-19: Beyond vLLM - Advanced data structures and performance patterns.

## Dependencies

**Imports** (29):
- `src.core.base.structures.BloomFilter.BloomFilter`
- `src.core.base.structures.BloomFilter.CountingBloomFilter`
- `src.core.base.structures.BloomFilter.ScalableBloomFilter`
- `src.core.base.structures.LockFreeQueue.BatchingQueue`
- `src.core.base.structures.LockFreeQueue.MPMCQueue`
- `src.core.base.structures.LockFreeQueue.PriorityQueue`
- `src.core.base.structures.LockFreeQueue.QueueStats`
- `src.core.base.structures.LockFreeQueue.SPSCQueue`
- `src.core.base.structures.LockFreeQueue.WorkStealingDeque`
- `src.core.base.structures.MemoryArena.ArenaStats`
- `src.core.base.structures.MemoryArena.MemoryArena`
- `src.core.base.structures.MemoryArena.SlabAllocator`
- `src.core.base.structures.MemoryArena.StackArena`
- `src.core.base.structures.MemoryArena.TypedArena`
- `src.core.base.structures.MemoryArena.temp_arena`
- ... and 14 more

---
*Auto-generated documentation*
## Source: src-old/core/base/structures/__init__.improvements.md

# Improvements for __init__

**File**: `src\\core\base\\structures\\__init__.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 85 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `__init___test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
Base data structures.

Phase 18-19: Beyond vLLM - Advanced data structures and performance patterns.
"""

from src.core.base.structures.BloomFilter import (
    BloomFilter,
    CountingBloomFilter,
    ScalableBloomFilter,
)
from src.core.base.structures.LockFreeQueue import (
    BatchingQueue,
    MPMCQueue,
    PriorityQueue,
    QueueStats,
    SPSCQueue,
    WorkStealingDeque,
)
from src.core.base.structures.MemoryArena import (
    ArenaStats,
    MemoryArena,
    SlabAllocator,
    StackArena,
    TypedArena,
    temp_arena,
    thread_temp_alloc,
)
from src.core.base.structures.ObjectPool import (
    BufferPool,
    ObjectPool,
    PoolStats,
    TieredBufferPool,
    TypedObjectPool,
    pooled_dict,
    pooled_list,
    pooled_set,
)
from src.core.base.structures.RingBuffer import (
    RingBuffer,
    SlidingWindowAggregator,
    ThreadSafeRingBuffer,
    TimeSeriesBuffer,
    TimestampedValue,
)

__all__ = [
    # Bloom Filters (Phase 18)
    "BloomFilter",
    "CountingBloomFilter",
    "ScalableBloomFilter",
    # Ring Buffers (Phase 18)
    "RingBuffer",
    "ThreadSafeRingBuffer",
    "TimeSeriesBuffer",
    "TimestampedValue",
    "SlidingWindowAggregator",
    # Object Pools (Phase 19)
    "ObjectPool",
    "TypedObjectPool",
    "BufferPool",
    "TieredBufferPool",
    "PoolStats",
    "pooled_list",
    "pooled_dict",
    "pooled_set",
    # Queues (Phase 19)
    "MPMCQueue",
    "SPSCQueue",
    "PriorityQueue",
    "WorkStealingDeque",
    "BatchingQueue",
    "QueueStats",
    # Memory Arenas (Phase 19)
    "MemoryArena",
    "TypedArena",
    "StackArena",
    "SlabAllocator",
    "ArenaStats",
    "temp_arena",
    "thread_temp_alloc",
]
