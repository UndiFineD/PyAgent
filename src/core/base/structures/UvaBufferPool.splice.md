# Class Breakdown: UvaBufferPool

**File**: `src\core\base\structures\UvaBufferPool.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BufferState`

**Line**: 47  
**Inherits**: Enum  
**Methods**: 0

State of a UVA buffer.

[TIP] **Suggested split**: Move to `bufferstate.py`

---

### 2. `AllocationStrategy`

**Line**: 55  
**Inherits**: Enum  
**Methods**: 0

Buffer allocation strategy.

[TIP] **Suggested split**: Move to `allocationstrategy.py`

---

### 3. `BufferStats`

**Line**: 63  
**Methods**: 2

Statistics for a single buffer.

[TIP] **Suggested split**: Move to `bufferstats.py`

---

### 4. `UvaBuffer`

**Line**: 88  
**Methods**: 10

A buffer with Unified Virtual Addressing for zero-copy GPU access.

UVA buffers use pinned (page-locked) host memory that can be directly
accessed by the GPU via PCIe without going through the CPU.

A...

[TIP] **Suggested split**: Move to `uvabuffer.py`

---

### 5. `UvaBufferPool`

**Line**: 310  
**Methods**: 14

Pool of UVA buffers with round-robin allocation.

This pool manages multiple UVA buffers for concurrent transfers,
allowing overlap of CPU-GPU copies with compute operations.

The pool supports adapti...

[TIP] **Suggested split**: Move to `uvabufferpool.py`

---

### 6. `UvaBackedTensor`

**Line**: 588  
**Methods**: 6

A tensor backed by UVA memory for automatic zero-copy transfers.

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
