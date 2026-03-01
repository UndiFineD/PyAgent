# Class Breakdown: input_buffer_manager

**File**: `src\infrastructure\compute\cuda\input_buffer_manager.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BufferState`

**Line**: 48  
**Inherits**: Enum  
**Methods**: 0

State of a buffer.

[TIP] **Suggested split**: Move to `bufferstate.py`

---

### 2. `BufferSpec`

**Line**: 58  
**Methods**: 2

Specification for a buffer.

[TIP] **Suggested split**: Move to `bufferspec.py`

---

### 3. `BufferEntry`

**Line**: 91  
**Methods**: 2

Entry in the buffer pool.

[TIP] **Suggested split**: Move to `bufferentry.py`

---

### 4. `BufferPool`

**Line**: 113  
**Inherits**: ABC  
**Methods**: 3

Abstract buffer pool interface.

[TIP] **Suggested split**: Move to `bufferpool.py`

---

### 5. `SimpleBufferPool`

**Line**: 129  
**Inherits**: BufferPool  
**Methods**: 6

Simple buffer pool implementation.

[TIP] **Suggested split**: Move to `simplebufferpool.py`

---

### 6. `InputSlot`

**Line**: 217  
**Methods**: 1

A slot for input data in the buffer.

[TIP] **Suggested split**: Move to `inputslot.py`

---

### 7. `InputBufferManager`

**Line**: 239  
**Methods**: 7

Manages input buffers for CUDA graph execution.

Based on vLLM's InputBatch pattern for pre-allocated
static buffers used during graph capture/replay.

[TIP] **Suggested split**: Move to `inputbuffermanager.py`

---

### 8. `HierarchicalBufferPool`

**Line**: 362  
**Inherits**: BufferPool  
**Methods**: 4

Hierarchical buffer pool.

Beyond vLLM:
- Multiple tiers (pinned CPU, GPU, managed)
- Automatic promotion/demotion

[TIP] **Suggested split**: Move to `hierarchicalbufferpool.py`

---

### 9. `PredictiveBufferManager`

**Line**: 399  
**Inherits**: InputBufferManager  
**Methods**: 4

Predictive buffer pre-allocation.

Beyond vLLM:
- Predicts future buffer needs
- Pre-warms buffers based on patterns

[TIP] **Suggested split**: Move to `predictivebuffermanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
