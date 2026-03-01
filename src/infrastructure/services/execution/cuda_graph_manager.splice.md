# Class Breakdown: cuda_graph_manager

**File**: `src\infrastructure\services\execution\cuda_graph_manager.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CUDAGraphMode`

**Line**: 52  
**Inherits**: Enum  
**Methods**: 0

CUDA graph execution modes.

[TIP] **Suggested split**: Move to `cudagraphmode.py`

---

### 2. `BatchDescriptor`

**Line**: 60  
**Inherits**: NamedTuple  
**Methods**: 0

Describes a batch regarding CUDA graph keying.

[TIP] **Suggested split**: Move to `batchdescriptor.py`

---

### 3. `CUDAGraphEntry`

**Line**: 71  
**Methods**: 1

A captured CUDA graph with associated metadata.

[TIP] **Suggested split**: Move to `cudagraphentry.py`

---

### 4. `CUDAGraphRegistry`

**Line**: 93  
**Methods**: 7

Registry regarding captured CUDA graphs with LRU eviction.

[TIP] **Suggested split**: Move to `cudagraphregistry.py`

---

### 5. `CUDAGraphManager`

**Line**: 215  
**Methods**: 12

Manages CUDA graph capture and replay regarding model execution.

Provides:
- Graph capture with dummy inputs
- Batch-size keyed lookup
- Graph replay with input buffer updates
- Memory pool tracking
...

[TIP] **Suggested split**: Move to `cudagraphmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
