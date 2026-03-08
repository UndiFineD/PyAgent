# StagedBatchWriter

**File**: `src\core\base\structures\StagedBatchWriter.py`  
**Type**: Python Module  
**Summary**: 6 classes, 2 functions, 16 imports  
**Lines**: 580  
**Complexity**: 25 (complex)

## Overview

StagedBatchWriter - Batched GPU writes with Triton kernel support.

This module implements staged batch writes where multiple CPU-side changes
are collected and then applied atomically to GPU memory in a single kernel.

Inspired by vLLM v1/worker/gpu/buffer_utils.py StagedWriteTensor, but extends with:
- Write coalescing for locality optimization
- Automatic power-of-2 growth for buffers
- Priority-based write ordering
- Memory pressure monitoring

Example:
    >>> writer = StagedBatchWriter(target_tensor=gpu_tensor)
    >>> writer.stage_write(idx=10, value=1.5)
    >>> writer.stage_write(idx=20, value=2.0)
    >>> writer.apply_writes(stream=cuda_stream)  # Batch apply via kernel

## Classes (6)

### `WritePolicy`

**Inherits from**: Enum

Policy for handling conflicting writes.

### `CoalesceStrategy`

**Inherits from**: Enum

Strategy for coalescing writes.

### `StagedWrite`

A single staged write operation.

### `WriteStats`

Statistics for write operations.

**Methods** (2):
- `avg_writes_per_apply(self)`
- `coalesce_ratio(self)`

### `StagedBatchWriter`

Collect writes and apply them in batch to GPU memory.

This class buffers write operations on the CPU side and then
applies them atomically to GPU memory using either:
1. Triton kernel for maximum performance
2. PyTorch scatter for compatibility
3. Rust-accelerated index computation

Attributes:
    target: Target tensor to write to
    capacity: Current buffer capacity
    policy: Conflict resolution policy
    coalesce: Coalescing strategy
    stats: Write statistics

**Methods** (11):
- `__init__(self, target, initial_capacity, max_capacity, policy, coalesce, block_size, use_triton, use_uva)`
- `_ensure_buffers(self, min_capacity)`
- `stage_write(self, index, value, priority)`
- `stage_writes(self, indices, values, priority)`
- `clear_staged(self)`
- `pending_count(self)`
- `_coalesce_writes(self)`
- `_resolve_conflict(self, writes)`
- `apply_writes(self, target, stream, sync)`
- `_apply_kernel(self, target, n_writes)`
- ... and 1 more methods

### `StagedWriteTensor`

A tensor with built-in staged write support.

This is a higher-level wrapper that combines a tensor with
a StagedBatchWriter for convenient write-batching.

**Methods** (10):
- `__init__(self, shape, dtype, device, fill_value)`
- `tensor(self)`
- `writer(self)`
- `__getitem__(self, key)`
- `stage_write(self, index, value, priority)`
- `stage_writes(self, indices, values, priority)`
- `apply(self, stream, sync)`
- `clear_staged(self)`
- `pending_count(self)`
- `stats(self)`

## Functions (2)

### `create_staged_tensor(shape, dtype, device)`

Create a staged write tensor.

### `coalesce_write_indices(indices, block_size)`

Reorder indices for memory locality.

Uses Rust acceleration if available.

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `math`
- `src.core.rust_bridge.get_bridge`
- `threading`
- `time`
- `torch`
- `triton`
- `triton.language`
- `typing.Any`
- `typing.Callable`
- `typing.Optional`
- ... and 1 more

---
*Auto-generated documentation*
