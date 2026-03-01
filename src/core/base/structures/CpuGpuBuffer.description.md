# CpuGpuBuffer

**File**: `src\core\base\structures\CpuGpuBuffer.py`  
**Type**: Python Module  
**Summary**: 2 classes, 2 functions, 7 imports  
**Lines**: 301  
**Complexity**: 19 (moderate)

## Overview

CpuGpuBuffer - Efficient CPU-GPU tensor transfer utilities.

Implements vLLM's CpuGpuBuffer pattern for paired CPU/GPU tensors
with non-blocking transfers and optional numpy views.

Phase 23: Advanced Serialization & Validation

## Classes (2)

### `CpuGpuBuffer`

Buffer for efficient tensor transfers between CPU and GPU.

Maintains paired CPU and GPU tensors of the same shape, enabling
fast non-blocking transfers. Optionally provides a numpy view of
the CPU tensor for efficient data manipulation.

Example:
    >>> buffer = CpuGpuBuffer(32, 768, dtype=torch.float32, device="cuda")
    >>> # Fill CPU buffer via numpy
    >>> buffer.np[:] = my_data
    >>> # Transfer to GPU (non-blocking)
    >>> gpu_tensor = buffer.copy_to_gpu()
    >>> # Use gpu_tensor in computation...
    >>> # Transfer results back
    >>> buffer.copy_to_cpu()
    >>> torch.cuda.synchronize()  # Required for CPU data to be valid

**Methods** (12):
- `__init__(self)`
- `copy_to_gpu(self, n, non_blocking)`
- `copy_to_cpu(self, n, non_blocking)`
- `fill(self, value)`
- `zero(self)`
- `resize(self)`
- `shape(self)`
- `dtype(self)`
- `device(self)`
- `numel(self)`
- ... and 2 more methods

### `CpuGpuBufferPool`

Pool of CpuGpuBuffers for efficient reuse.

Maintains a pool of pre-allocated buffers to avoid repeated allocation.

**Methods** (5):
- `__init__(self, size, dtype, device, pool_size)`
- `acquire(self)`
- `release(self, handle)`
- `available(self)`
- `total(self)`

## Functions (2)

### `is_pin_memory_available()`

Check if CUDA pinned memory is available.

### `get_device(device)`

Get a torch device.

Args:
    device: Device specification (None = auto-detect)
    
Returns:
    torch.device instance

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `numpy`
- `torch`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
