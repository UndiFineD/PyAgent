# CpuGpuBufferPool

**File**: `src\infrastructure\execution\CpuGpuBufferPool.py`  
**Type**: Python Module  
**Summary**: 4 classes, 6 functions, 11 imports  
**Lines**: 411  
**Complexity**: 33 (complex)

## Overview

CpuGpuBufferPool.py - Paired CPU/GPU tensor buffers.

Inspired by vLLM's v1/worker/gpu/buffer_utils.py. Provides unified
buffer management for CPU/GPU memory with efficient pinned memory
transfers.

Phase 29: Execution Context, Batching & Async Streaming

## Classes (4)

### `MemoryPlacement`

**Inherits from**: Enum

Memory placement options.

### `CpuGpuBuffer`

A paired CPU/GPU buffer for efficient data transfer.

Maintains both CPU and GPU views of the same data.
Based on vLLM's CpuGpuBuffer pattern.

**Methods** (12):
- `__post_init__(self)`
- `allocate(cls, name, shape, dtype, pinned)`
- `cpu_to_gpu(self)`
- `gpu_to_cpu(self)`
- `sync(self)`
- `mark_cpu_dirty(self)`
- `mark_gpu_dirty(self)`
- `fill(self, value)`
- `reset(self)`
- `slice(self)`
- ... and 2 more methods

### `UvaBufferPool`

Pool of CPU/GPU buffers for efficient reuse.

Manages a collection of buffers with unified virtual addressing pattern.
Based on vLLM's UvaBufferPool pattern.

**Methods** (9):
- `__init__(self, name)`
- `allocate(self, name, shape, dtype, pinned)`
- `get(self, name)`
- `release(self, name)`
- `clear(self)`
- `total_bytes(self)`
- `num_buffers(self)`
- `sync_all(self)`
- `stats(self)`

### `PinnedMemoryManager`

Manager for pinned (page-locked) memory buffers.

Pinned memory enables faster CPU-GPU transfers.

**Methods** (6):
- `__init__(self, max_bytes)`
- `allocate(self, shape, dtype)`
- `free(self, buf)`
- `clear(self)`
- `allocated_bytes(self)`
- `available_bytes(self)`

## Functions (6)

### `copy_with_indices(src, dst, indices)`

Copy data from src to dst using index mapping.

dst[i] = src[indices[i]] for all i.

### `scatter_with_indices(src, dst, indices)`

Scatter data from src to dst using index mapping.

dst[indices[i]] = src[i] for all i.

### `pad_to_multiple(arr, multiple, axis, pad_value)`

Pad array to a multiple of given value along axis.

### `compute_cumsum_offsets(lengths)`

Compute cumulative sum offsets from lengths.

Returns array of length len(lengths) + 1 with offsets.

### `flatten_with_offsets(arrays)`

Flatten a list of arrays into one with offsets.

Returns (flattened, offsets).

### `split_by_offsets(arr, offsets)`

Split an array by offset boundaries.

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `numpy`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
