# Class Breakdown: ForwardContext

**File**: `src\infrastructure\execution\ForwardContext.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BatchDescriptor`

**Line**: 26  
**Inherits**: NamedTuple  
**Methods**: 4

Batch descriptor for CUDA graph dispatching.

Uniquely identifies a padded batch configuration for graph key matching.
Based on vLLM's BatchDescriptor pattern.

[TIP] **Suggested split**: Move to `batchdescriptor.py`

---

### 2. `DPMetadata`

**Line**: 73  
**Methods**: 4

Data parallel metadata for distributed inference.

Tracks token distribution across data parallel ranks for synchronization.
Based on vLLM's DPMetadata pattern.

[TIP] **Suggested split**: Move to `dpmetadata.py`

---

### 3. `ForwardContext`

**Line**: 135  
**Methods**: 4

Thread-local context for model forward passes.

Stores attention metadata, batch descriptors, and coordination info
that needs to be accessed during forward execution.

Based on vLLM's ForwardContext ...

[TIP] **Suggested split**: Move to `forwardcontext.py`

---

### 4. `ForwardTimingTracker`

**Line**: 326  
**Methods**: 5

Tracks forward pass timing statistics.

Provides batch size to latency mapping for performance analysis.

[TIP] **Suggested split**: Move to `forwardtimingtracker.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
