# Class Breakdown: cuda_graph_manager

**File**: `src\infrastructure\compute\cuda\cuda_graph_manager.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CUDAGraphMode`

**Line**: 41  
**Inherits**: IntEnum  
**Methods**: 2

CUDA graph execution modes.

[TIP] **Suggested split**: Move to `cudagraphmode.py`

---

### 2. `BatchDescriptor`

**Line**: 58  
**Methods**: 2

Key for CUDA graph cache lookup.

Attributes:
    num_tokens: Number of tokens in batch
    num_reqs: Number of requests (optional)
    is_uniform_decode: Whether batch is uniform decode

[TIP] **Suggested split**: Move to `batchdescriptor.py`

---

### 3. `CUDAGraphEntry`

**Line**: 81  
**Methods**: 1

Cached CUDA graph entry with metadata.

Attributes:
    batch_descriptor: Key for this entry
    cudagraph: The captured CUDA graph (mock for non-GPU)
    output: Weak reference to output tensors
    ...

[TIP] **Suggested split**: Move to `cudagraphentry.py`

---

### 4. `CUDAGraphOptions`

**Line**: 107  
**Methods**: 0

Options for CUDA graph wrapper behavior.

[TIP] **Suggested split**: Move to `cudagraphoptions.py`

---

### 5. `CUDAGraphStats`

**Line**: 117  
**Methods**: 1

Statistics for CUDA graph usage.

[TIP] **Suggested split**: Move to `cudagraphstats.py`

---

### 6. `MockCUDAGraph`

**Line**: 132  
**Methods**: 4

Mock CUDA graph for non-GPU environments.

[TIP] **Suggested split**: Move to `mockcudagraph.py`

---

### 7. `CUDAGraphWrapper`

**Line**: 153  
**Methods**: 12

Wraps a callable to add CUDA graph capture/replay.

Based on vLLM's CUDAGraphWrapper from cuda_graph.py.
Provides automatic graph caching, capture, and replay
based on batch descriptors.

Beyond vLLM:...

[TIP] **Suggested split**: Move to `cudagraphwrapper.py`

---

### 8. `AdaptiveCUDAGraphWrapper`

**Line**: 364  
**Inherits**: CUDAGraphWrapper  
**Methods**: 5

Extended wrapper with adaptive capture based on usage patterns.

Beyond vLLM:
- Tracks shape frequency to prioritize common shapes
- Predictive pre-warming of likely shapes
- Memory budget awareness

[TIP] **Suggested split**: Move to `adaptivecudagraphwrapper.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
