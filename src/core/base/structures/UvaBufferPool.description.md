# UvaBufferPool

**File**: `src\core\base\structures\UvaBufferPool.py`  
**Type**: Python Module  
**Summary**: 6 classes, 2 functions, 15 imports  
**Lines**: 685  
**Complexity**: 34 (complex)

## Overview

UvaBufferPool - Zero-copy GPU transfers via Unified Virtual Addressing.

This module implements UVA (Unified Virtual Addressing) buffer management
for efficient CPU-GPU data transfers without intermediate copies.

Inspired by vLLM v1/worker/gpu/buffer_utils.py, but extends with:
- Adaptive pool sizing based on access patterns
- Priority-aware buffer allocation
- Memory pressure monitoring
- Automatic buffer promotion/demotion

Example:
    >>> pool = UvaBufferPool(buffer_count=4, buffer_size=1024*1024)
    >>> buffer = pool.acquire()
    >>> buffer.copy_to_uva(cpu_tensor)  # Zero-copy to GPU-visible memory
    >>> buffer.copy_to_gpu(cuda_stream)  # DMA transfer to GPU
    >>> pool.release(buffer)

## Classes (6)

### `BufferState`

**Inherits from**: Enum

State of a UVA buffer.

### `AllocationStrategy`

**Inherits from**: Enum

Buffer allocation strategy.

### `BufferStats`

Statistics for a single buffer.

**Methods** (2):
- `avg_transfer_time_ms(self)`
- `throughput_gbps(self)`

### `UvaBuffer`

A buffer with Unified Virtual Addressing for zero-copy GPU access.

UVA buffers use pinned (page-locked) host memory that can be directly
accessed by the GPU via PCIe without going through the CPU.

Attributes:
    buffer_id: Unique identifier for this buffer
    size: Size in bytes
    cpu_tensor: CPU-side tensor (pinned memory)
    uva_tensor: GPU-visible view of the CPU tensor
    dtype: Data type of the buffer
    state: Current buffer state
    stats: Usage statistics

**Methods** (10):
- `__post_init__(self)`
- `_initialize_tensors(self)`
- `cpu_tensor(self)`
- `uva_tensor(self)`
- `gpu_tensor(self)`
- `copy_to_uva(self, data)`
- `copy_to_gpu(self, stream, non_blocking)`
- `copy_to_cpu(self, stream, non_blocking)`
- `sync(self, stream)`
- `reset(self)`

### `UvaBufferPool`

Pool of UVA buffers with round-robin allocation.

This pool manages multiple UVA buffers for concurrent transfers,
allowing overlap of CPU-GPU copies with compute operations.

The pool supports adaptive sizing based on access patterns,
going beyond vLLM's fixed pool approach.

Attributes:
    buffer_count: Number of buffers in the pool
    buffer_size: Size of each buffer in bytes
    strategy: Allocation strategy

**Methods** (14):
- `__init__(self, buffer_count, buffer_size, dtype, strategy, max_buffers, grow_factor, shrink_threshold)`
- `_initialize_pool(self)`
- `acquire(self, priority, blocking, timeout)`
- `_try_acquire(self, priority)`
- `_acquire_round_robin(self, priority)`
- `_acquire_least_recent(self, priority)`
- `_acquire_priority(self, priority)`
- `release(self, buffer)`
- `_should_grow(self)`
- `_grow_pool(self)`
- ... and 4 more methods

### `UvaBackedTensor`

A tensor backed by UVA memory for automatic zero-copy transfers.

This is a higher-level wrapper that automatically manages UVA buffer
allocation and provides a tensor-like interface.

**Methods** (6):
- `__init__(self, shape, dtype, pool)`
- `fill(self, data)`
- `to_gpu(self, stream)`
- `to_cpu(self, stream)`
- `sync(self)`
- `__del__(self)`

## Functions (2)

### `create_uva_buffer(size, dtype)`

Create a single UVA buffer.

### `create_uva_pool(count, size, dtype)`

Create a UVA buffer pool.

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `collections.deque`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `math`
- `numpy`
- `src.core.rust_bridge.get_bridge`
- `threading`
- `time`
- `torch`
- `typing.Any`
- `typing.Callable`
- `typing.Optional`

---
*Auto-generated documentation*
