# MicroBatchContext

**File**: `src\core\base\core\MicroBatchContext.py`  
**Type**: Python Module  
**Summary**: 7 classes, 2 functions, 17 imports  
**Lines**: 529  
**Complexity**: 28 (complex)

## Overview

MicroBatchContext - Micro-batch orchestration with CUDA stream synchronization.

This module implements thread-synchronized micro-batching for efficient
GPU utilization with separate compute and communication streams.

Inspired by vLLM v1/worker/ubatching.py UBatchContext, but extends with:
- Adaptive scheduling based on batch size and memory pressure
- Priority-based micro-batch ordering
- Dynamic stream selection based on workload
- Context state preservation across micro-batches

Example:
    >>> with MicroBatchContext(batch_size=32, micro_batch_size=8) as ctx:
    ...     for micro_batch in ctx.iterate():
    ...         result = model(micro_batch)
    ...         ctx.record_output(result)
    >>> final = ctx.gather_outputs()

## Classes (7)

### `StreamType`

**Inherits from**: Enum

Type of CUDA stream.

### `MicroBatchState`

**Inherits from**: Enum

State of a micro-batch.

### `StreamHandle`

Handle to a CUDA stream with metadata.

**Methods** (3):
- `synchronize(self)`
- `record_event(self, event)`
- `wait_event(self, event)`

### `MicroBatchInfo`

Information about a single micro-batch.

**Methods** (1):
- `duration_ms(self)`

### `StreamManager`

Manages CUDA streams for compute and communication.

This class maintains separate stream pools for compute and
communication operations, enabling overlap of transfers with compute.

**Methods** (7):
- `__init__(self, num_compute_streams, num_comm_streams, use_high_priority)`
- `_initialize_streams(self)`
- `get_compute_stream(self)`
- `get_comm_stream(self)`
- `synchronize_all(self)`
- `compute_context(self)`
- `comm_context(self)`

### `MicroBatchContext`

**Inherits from**: Unknown

Thread-synchronized micro-batch context.

This context manager handles the orchestration of micro-batches
with proper CUDA stream synchronization and thread barriers.

Attributes:
    batch_size: Total batch size
    micro_batch_size: Size of each micro-batch
    num_micro_batches: Number of micro-batches

**Methods** (12):
- `__init__(self, batch_size, micro_batch_size, num_threads, stream_manager, adaptive, min_micro_batch, max_micro_batch)`
- `_init_micro_batches(self)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`
- `iterate(self)`
- `iterate_with_data(self, data)`
- `record_output(self, output, mb_idx)`
- `gather_outputs(self)`
- `gather_and_concat(self)`
- `sync_streams(self)`
- ... and 2 more methods

### `AdaptiveMicroBatchContext`

**Inherits from**: Unknown

Micro-batch context with adaptive sizing.

This extends MicroBatchContext to dynamically adjust micro-batch
sizes based on memory pressure and execution times.

**Methods** (3):
- `__init__(self, batch_size, initial_micro_batch, target_time_ms, memory_threshold)`
- `_adapt_size(self)`
- `iterate(self)`

## Functions (2)

### `create_micro_batch_context(batch_size, micro_batch_size, adaptive)`

Create a micro-batch context.

Args:
    batch_size: Total batch size
    micro_batch_size: Size of each micro-batch
    adaptive: Whether to use adaptive sizing
    **kwargs: Additional arguments
    
Returns:
    MicroBatchContext instance

### `micro_batch_scope(batch_size, micro_batch_size)`

Context manager for micro-batching.

Usage:
    >>> with micro_batch_scope(100, 10) as ctx:
    ...     for mb in ctx.iterate():
    ...         process(mb)

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `contextlib.contextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `queue`
- `src.core.rust_bridge.get_bridge`
- `threading`
- `time`
- `torch`
- `typing.Any`
- `typing.Callable`
- `typing.Generic`
- `typing.Iterator`
- ... and 2 more

---
*Auto-generated documentation*
