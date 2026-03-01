# Class Breakdown: GPUMemoryAllocator

**File**: `src\infrastructure\memory\GPUMemoryAllocator.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MemoryState`

**Line**: 28  
**Inherits**: Enum  
**Methods**: 0

GPU memory allocator state.

[TIP] **Suggested split**: Move to `memorystate.py`

---

### 2. `AllocationStrategy`

**Line**: 35  
**Inherits**: Enum  
**Methods**: 0

Memory allocation strategy.

[TIP] **Suggested split**: Move to `allocationstrategy.py`

---

### 3. `MemoryRegion`

**Line**: 44  
**Methods**: 1

A memory region/allocation.

[TIP] **Suggested split**: Move to `memoryregion.py`

---

### 4. `MemorySnapshot`

**Line**: 62  
**Methods**: 1

Snapshot of GPU memory state.

vLLM Pattern: MemorySnapshot for state capture/restore

[TIP] **Suggested split**: Move to `memorysnapshot.py`

---

### 5. `MemoryPoolConfig`

**Line**: 93  
**Methods**: 0

Configuration for memory pool.

[TIP] **Suggested split**: Move to `memorypoolconfig.py`

---

### 6. `MemoryPressureEvent`

**Line**: 104  
**Methods**: 1

Event for memory pressure notifications.

[TIP] **Suggested split**: Move to `memorypressureevent.py`

---

### 7. `CuMemAllocator`

**Line**: 115  
**Methods**: 20

Custom CUDA memory allocator with sleep/wake support.

vLLM Pattern: CuMemAllocator from cumem.py

Beyond vLLM:
- Multi-GPU memory balancing
- Pressure-aware allocation
- Automatic defragmentation

[TIP] **Suggested split**: Move to `cumemallocator.py`

---

### 8. `MultiGPUMemoryBalancer`

**Line**: 566  
**Methods**: 7

Balance memory allocation across multiple GPUs.

Beyond vLLM: Multi-GPU memory coordination.

[TIP] **Suggested split**: Move to `multigpumemorybalancer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
