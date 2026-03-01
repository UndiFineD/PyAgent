# Class Breakdown: WeightLoader

**File**: `src\infrastructure\loading\WeightLoader.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `WeightFormat`

**Line**: 60  
**Inherits**: Enum  
**Methods**: 0

Supported weight file formats.

[TIP] **Suggested split**: Move to `weightformat.py`

---

### 2. `WeightSpec`

**Line**: 71  
**Methods**: 2

Specification for a weight tensor.

[TIP] **Suggested split**: Move to `weightspec.py`

---

### 3. `LoadStats`

**Line**: 93  
**Methods**: 1

Statistics for weight loading.

[TIP] **Suggested split**: Move to `loadstats.py`

---

### 4. `AtomicWriter`

**Line**: 109  
**Methods**: 3

Context manager for atomic file writing.

Writes to a temporary file first, then atomically replaces the target.
This ensures the target file is never left in a corrupted state.

vLLM Pattern: atomic_...

[TIP] **Suggested split**: Move to `atomicwriter.py`

---

### 5. `WeightLoader`

**Line**: 207  
**Inherits**: ABC  
**Methods**: 3

Abstract base class for weight loaders.

Defines the interface for loading model weights from various sources.

[TIP] **Suggested split**: Move to `weightloader.py`

---

### 6. `SafetensorsLoader`

**Line**: 237  
**Inherits**: WeightLoader  
**Methods**: 3

Loader for safetensors files.

Supports lazy (default) and eager loading strategies.
vLLM Pattern: safetensors_weights_iterator

[TIP] **Suggested split**: Move to `safetensorsloader.py`

---

### 7. `MultiThreadWeightLoader`

**Line**: 297  
**Inherits**: WeightLoader  
**Methods**: 6

Multi-threaded weight loader for parallel file loading.

vLLM Pattern: multi_thread_safetensors_weights_iterator
BEYOND vLLM: Adaptive worker count based on file count/size

[TIP] **Suggested split**: Move to `multithreadweightloader.py`

---

### 8. `FastSafetensorsLoader`

**Line**: 379  
**Inherits**: WeightLoader  
**Methods**: 3

Fast safetensors loader using GPU direct storage.

vLLM Pattern: fastsafetensors_weights_iterator
Uses fastsafetensors library for direct GPU loading with GDS support.

[TIP] **Suggested split**: Move to `fastsafetensorsloader.py`

---

### 9. `StreamingWeightLoader`

**Line**: 440  
**Inherits**: WeightLoader  
**Methods**: 5

Streaming weight loader for memory-constrained environments.

BEYOND vLLM: Loads weights in batches with configurable memory budget,
supports predictive prefetching and priority-based loading.

[TIP] **Suggested split**: Move to `streamingweightloader.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
