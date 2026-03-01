# Class Breakdown: CudagraphDispatcher

**File**: `src\infrastructure\cuda\CudagraphDispatcher.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DispatchMode`

**Line**: 31  
**Inherits**: Enum  
**Methods**: 0

Mode of execution dispatch.

[TIP] **Suggested split**: Move to `dispatchmode.py`

---

### 2. `DispatchKey`

**Line**: 40  
**Methods**: 1

Key for dispatch decisions.

Attributes:
    num_tokens: Number of tokens in batch
    num_reqs: Number of requests
    max_seq_len: Maximum sequence length
    is_prefill: Whether this is prefill pha...

[TIP] **Suggested split**: Move to `dispatchkey.py`

---

### 3. `DispatchStats`

**Line**: 60  
**Methods**: 1

Statistics for dispatch decisions.

[TIP] **Suggested split**: Move to `dispatchstats.py`

---

### 4. `DispatchPolicy`

**Line**: 77  
**Inherits**: ABC  
**Methods**: 2

Abstract dispatch policy.

[TIP] **Suggested split**: Move to `dispatchpolicy.py`

---

### 5. `DefaultDispatchPolicy`

**Line**: 99  
**Inherits**: DispatchPolicy  
**Methods**: 3

Default policy preferring graphs when available.

[TIP] **Suggested split**: Move to `defaultdispatchpolicy.py`

---

### 6. `AdaptiveDispatchPolicy`

**Line**: 138  
**Inherits**: DispatchPolicy  
**Methods**: 4

Adaptive policy learning from history.

Beyond vLLM:
- Learns optimal dispatch based on performance history
- Adjusts thresholds dynamically

[TIP] **Suggested split**: Move to `adaptivedispatchpolicy.py`

---

### 7. `GraphEntry`

**Line**: 203  
**Methods**: 0

Entry in the graph cache.

[TIP] **Suggested split**: Move to `graphentry.py`

---

### 8. `CudagraphDispatcher`

**Line**: 212  
**Methods**: 11

Dispatcher for CUDA graph execution.

Manages graph selection, fallback logic, and execution
based on vLLM's dispatch patterns.

[TIP] **Suggested split**: Move to `cudagraphdispatcher.py`

---

### 9. `CompositeDispatcher`

**Line**: 392  
**Methods**: 3

Composite dispatcher supporting multiple strategies.

Beyond vLLM:
- Chains multiple dispatchers
- Priority-based selection
- Fallback chains

[TIP] **Suggested split**: Move to `compositedispatcher.py`

---

### 10. `StreamDispatcher`

**Line**: 441  
**Inherits**: CudagraphDispatcher  
**Methods**: 3

Multi-stream dispatcher.

Beyond vLLM:
- Dispatches to different CUDA streams
- Stream-local graph caching

[TIP] **Suggested split**: Move to `streamdispatcher.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
