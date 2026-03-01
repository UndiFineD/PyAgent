# Class Breakdown: cpu_gpu_buffer

**File**: `src\core\base\logic\structures\cpu_gpu_buffer.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CpuGpuBuffer`

**Line**: 83  
**Methods**: 12

Buffer for efficient tensor transfers between CPU and GPU.

Maintains paired CPU and GPU tensors of the same shape, enabling
fast non-blocking transfers. Optionally provides a numpy view of
the CPU te...

[TIP] **Suggested split**: Move to `cpugpubuffer.py`

---

### 2. `CpuGpuBufferPool`

**Line**: 247  
**Methods**: 5

Pool of CpuGpuBuffers for efficient reuse.

Maintains a pool of pre-allocated buffers to avoid repeated allocation.

[TIP] **Suggested split**: Move to `cpugpubufferpool.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
