# GPUMemoryAllocator

**File**: `src\infrastructure\memory\GPUMemoryAllocator.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 16 imports  
**Lines**: 659  
**Complexity**: 30 (complex)

## Overview

GPUMemoryAllocator: GPU memory optimization with sleep/wake and pooling.

vLLM Pattern: CuMemAllocator from v1/core/gpu_memory/cumem.py
- sleep() / wake_up() for GPU memory sharing
- use_memory_pool() context manager
- MemorySnapshot for state capture/restore

Beyond vLLM:
- Multi-GPU memory balancing
- Memory pressure detection and response
- Automatic fragmentation management

## Classes (8)

### `MemoryState`

**Inherits from**: Enum

GPU memory allocator state.

### `AllocationStrategy`

**Inherits from**: Enum

Memory allocation strategy.

### `MemoryRegion`

A memory region/allocation.

**Methods** (1):
- `touch(self)`

### `MemorySnapshot`

Snapshot of GPU memory state.

vLLM Pattern: MemorySnapshot for state capture/restore

**Methods** (1):
- `to_dict(self)`

### `MemoryPoolConfig`

Configuration for memory pool.

### `MemoryPressureEvent`

Event for memory pressure notifications.

**Methods** (1):
- `__init__(self, device_id, available_bytes, total_bytes)`

### `CuMemAllocator`

Custom CUDA memory allocator with sleep/wake support.

vLLM Pattern: CuMemAllocator from cumem.py

Beyond vLLM:
- Multi-GPU memory balancing
- Pressure-aware allocation
- Automatic defragmentation

**Methods** (20):
- `__init__(self, config)`
- `_init_pool(self)`
- `allocate(self, size_bytes)`
- `_allocate_pool(self, size_bytes)`
- `_allocate_best_fit(self, size_bytes)`
- `deallocate(self, region_id)`
- `sleep(self)`
- `wake_up(self)`
- `use_memory_pool(self)`
- `take_snapshot(self)`
- ... and 10 more methods

### `MultiGPUMemoryBalancer`

Balance memory allocation across multiple GPUs.

Beyond vLLM: Multi-GPU memory coordination.

**Methods** (7):
- `__init__(self, num_devices)`
- `get_allocator(self, device_id)`
- `allocate_balanced(self, size_bytes)`
- `deallocate(self, device_id, region_id)`
- `sleep_all(self)`
- `wake_up_all(self)`
- `get_total_stats(self)`

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `contextlib.contextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `logging`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Generator`
- `typing.List`
- `typing.Optional`
- ... and 1 more

---
*Auto-generated documentation*
