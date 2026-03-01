# Class Breakdown: CUDAGraphManager

**File**: `src\infrastructure\execution\CUDAGraphManager.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CUDAGraphMode`

**Line**: 37  
**Inherits**: Enum  
**Methods**: 0

CUDA graph execution modes.

[TIP] **Suggested split**: Move to `cudagraphmode.py`

---

### 2. `BatchDescriptor`

**Line**: 44  
**Inherits**: NamedTuple  
**Methods**: 0

Describes a batch for CUDA graph keying.

[TIP] **Suggested split**: Move to `batchdescriptor.py`

---

### 3. `CUDAGraphEntry`

**Line**: 54  
**Methods**: 1

A captured CUDA graph with associated metadata.

[TIP] **Suggested split**: Move to `cudagraphentry.py`

---

### 4. `CUDAGraphRegistry`

**Line**: 75  
**Methods**: 7

Registry of captured CUDA graphs with LRU eviction.

[TIP] **Suggested split**: Move to `cudagraphregistry.py`

---

### 5. `CUDAGraphManager`

**Line**: 206  
**Methods**: 12

Manages CUDA graph capture and replay for model execution.

Provides:
- Graph capture with dummy inputs
- Batch-size keyed lookup
- Graph replay with input buffer updates
- Memory pool tracking
- LRU ...

[TIP] **Suggested split**: Move to `cudagraphmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
