# CudaStreamPool

**File**: `src\core\base\core\CudaStreamPool.py`  
**Type**: Python Module  
**Summary**: 7 classes, 5 functions, 16 imports  
**Lines**: 641  
**Complexity**: 42 (complex)

## Overview

CudaStreamPool - CUDA stream and event management with pooling.

This module provides efficient stream and event pooling for GPU operations,
enabling better overlap of compute and communication.

Inspired by vLLM's stream management, but extends with:
- Priority stream hints for latency-critical operations
- Automatic cleanup on pool destruction
- Stream affinity for related operations
- Event recycling to reduce allocation overhead

Example:
    >>> pool = CudaStreamPool(compute_streams=4, comm_streams=2)
    >>> with pool.acquire_compute() as stream:
    ...     result = model(input, stream=stream)
    >>> pool.sync_all()

## Classes (7)

### `StreamPriority`

**Inherits from**: Enum

Priority level for CUDA streams.

### `StreamState`

**Inherits from**: Enum

State of a pooled stream.

### `StreamStats`

Statistics for a stream.

**Methods** (1):
- `avg_active_time_ms(self)`

### `PooledStream`

A CUDA stream managed by a pool.

Attributes:
    stream_id: Unique identifier
    priority: Stream priority
    state: Current state
    stream: Underlying CUDA stream

**Methods** (6):
- `__post_init__(self)`
- `_get_cuda_priority(self)`
- `synchronize(self)`
- `query(self)`
- `wait_event(self, event)`
- `context(self)`

### `PooledEvent`

A CUDA event managed by a pool.

Attributes:
    event_id: Unique identifier
    event: Underlying CUDA event

**Methods** (5):
- `__post_init__(self)`
- `record(self, stream)`
- `synchronize(self)`
- `query(self)`
- `elapsed_time(self, end_event)`

### `EventPool`

Pool of reusable CUDA events.

Events are expensive to create, so pooling them improves performance.

**Methods** (6):
- `__init__(self, initial_size, max_size)`
- `_create_event(self)`
- `acquire(self)`
- `release(self, event)`
- `event_context(self)`
- `clear(self)`

### `CudaStreamPool`

Pool of CUDA streams for compute and communication.

This pool manages separate stream pools for different operation
types, enabling efficient overlap of compute with data transfers.

Attributes:
    compute_streams: Number of compute streams
    comm_streams: Number of communication streams

**Methods** (19):
- `__init__(self, compute_streams, comm_streams, high_priority_streams, event_pool_size, enable_affinity)`
- `_initialize_pools(self)`
- `acquire_compute(self, affinity_key, blocking, timeout)`
- `acquire_comm(self, affinity_key, blocking, timeout)`
- `acquire_high_priority(self, blocking, timeout)`
- `_acquire_from_pool(self, pool, affinity_key, blocking, timeout)`
- `_mark_acquired(self, stream, pool, affinity_key)`
- `release(self, stream)`
- `compute_context(self, affinity_key)`
- `comm_context(self, affinity_key)`
- ... and 9 more methods

## Functions (5)

### `get_global_stream_pool(compute_streams, comm_streams)`

Get or create global stream pool.

Args:
    compute_streams: Number of compute streams (only used on creation)
    comm_streams: Number of comm streams (only used on creation)
    
Returns:
    Global CudaStreamPool instance

### `reset_global_pool()`

Reset the global stream pool.

### `compute_stream(affinity_key)`

Get a compute stream from the global pool.

### `comm_stream(affinity_key)`

Get a communication stream from the global pool.

### `high_priority_stream()`

Get a high-priority stream from the global pool.

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `collections.deque`
- `contextlib.contextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `src.core.rust_bridge.get_bridge`
- `threading`
- `time`
- `torch`
- `typing.Any`
- `typing.Callable`
- `typing.Iterator`
- `typing.Optional`
- ... and 1 more

---
*Auto-generated documentation*
