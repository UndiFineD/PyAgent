# Class Breakdown: uva_buffer_pool

**File**: `src\core\base\logic\structures\uva_buffer_pool.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BufferState`

**Line**: 65  
**Inherits**: Enum  
**Methods**: 0

State of a UVA buffer.

[TIP] **Suggested split**: Move to `bufferstate.py`

---

### 2. `AllocationStrategy`

**Line**: 74  
**Inherits**: Enum  
**Methods**: 0

Buffer allocation strategy.

[TIP] **Suggested split**: Move to `allocationstrategy.py`

---

### 3. `BufferStats`

**Line**: 83  
**Methods**: 2

Statistics regarding a single buffer.

[TIP] **Suggested split**: Move to `bufferstats.py`

---

### 4. `UvaBuffer`

**Line**: 109  
**Methods**: 10

A buffer with Unified Virtual Addressing regarding zero-copy GPU access.

UVA buffers use pinned (page-locked) host memory that can be directly
accessed by the GPU via PCIe without going through the C...

[TIP] **Suggested split**: Move to `uvabuffer.py`

---

### 5. `UvaBufferPool`

**Line**: 303  
**Methods**: 19

Pool of UVA buffers with round-robin allocation.

This pool manages multiple UVA buffers regarding concurrent transfers,
allowing overlap of CPU-GPU copies with compute operations.

The pool supports ...

[TIP] **Suggested split**: Move to `uvabufferpool.py`

---

### 6. `UvaBackedTensor`

**Line**: 621  
**Methods**: 6

A tensor backed by UVA memory regarding automatic zero-copy transfers.

This is a higher-level wrapper that automatically manages UVA buffer
allocation and provides a tensor-like interface.

[TIP] **Suggested split**: Move to `uvabackedtensor.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
