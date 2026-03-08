# LockFreeQueue

**File**: `src\core\base\structures\LockFreeQueue.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 17 imports  
**Lines**: 649  
**Complexity**: 42 (complex)

## Overview

Lock-Free Queue for high-performance concurrent operations.

Phase 19: Beyond vLLM - Performance Patterns
Wait-free and lock-free data structures.

## Classes (7)

### `QueueStats`

Statistics for queue operations.

**Methods** (2):
- `current_size(self)`
- `to_dict(self)`

### `MPMCQueue`

**Inherits from**: Unknown

Multi-Producer Multi-Consumer bounded queue.

High-performance queue optimized for concurrent access.
Uses fine-grained locking with separate locks for head/tail.

Features:
- Bounded capacity to prevent memory exhaustion
- Non-blocking try_* operations
- Blocking operations with timeout
- Statistics tracking

Example:
    queue = MPMCQueue[int](capacity=1000)
    
    # Producer
    queue.put(42)
    
    # Consumer
    value = queue.get()

**Methods** (13):
- `__init__(self, capacity)`
- `put(self, item, timeout)`
- `try_put(self, item)`
- `get(self, timeout)`
- `try_get(self)`
- `peek(self)`
- `close(self)`
- `clear(self)`
- `is_closed(self)`
- `__len__(self)`
- ... and 3 more methods

### `SPSCQueue`

**Inherits from**: Unknown

Single-Producer Single-Consumer lock-free queue.

Optimized for scenarios with exactly one producer and one consumer thread.
Uses memory barriers instead of locks for maximum performance.

WARNING: Only safe with exactly one producer and one consumer thread!

**Methods** (7):
- `__init__(self, capacity)`
- `try_put(self, item)`
- `try_get(self)`
- `size(self)`
- `is_empty(self)`
- `is_full(self)`
- `stats(self)`

### `PriorityItem`

**Inherits from**: Unknown

Item with priority for priority queue.

### `PriorityQueue`

**Inherits from**: Unknown

Thread-safe priority queue.

Lower priority values are dequeued first (min-heap).
Maintains FIFO order for items with equal priority.

**Methods** (8):
- `__init__(self, capacity)`
- `put(self, item, priority, timeout)`
- `get(self, timeout)`
- `try_get(self)`
- `peek(self)`
- `size(self)`
- `__len__(self)`
- `stats(self)`

### `WorkStealingDeque`

**Inherits from**: Unknown

Work-stealing deque for task scheduling.

Owner pushes/pops from tail (LIFO for cache locality).
Thieves steal from head (FIFO to get older tasks).

**Methods** (7):
- `__init__(self, capacity)`
- `push(self, item)`
- `pop(self)`
- `steal(self)`
- `size(self)`
- `is_empty(self)`
- `stats(self)`

### `BatchingQueue`

**Inherits from**: Unknown

Queue that batches items for efficient processing.

Collects items until batch size or timeout is reached,
then delivers as a batch.

**Methods** (5):
- `__init__(self, batch_size, batch_timeout, max_pending)`
- `put(self, item)`
- `get_batch(self, timeout)`
- `pending_count(self)`
- `stats(self)`

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `collections.deque`
- `dataclasses.dataclass`
- `dataclasses.field`
- `heapq`
- `queue.Empty`
- `queue.Full`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Generic`
- `typing.Iterator`
- `typing.List`
- ... and 2 more

---
*Auto-generated documentation*
