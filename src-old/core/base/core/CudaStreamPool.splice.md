# Class Breakdown: CudaStreamPool

**File**: `src\core\base\core\CudaStreamPool.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StreamPriority`

**Line**: 50  
**Inherits**: Enum  
**Methods**: 0

Priority level for CUDA streams.

[TIP] **Suggested split**: Move to `streampriority.py`

---

### 2. `StreamState`

**Line**: 57  
**Inherits**: Enum  
**Methods**: 0

State of a pooled stream.

[TIP] **Suggested split**: Move to `streamstate.py`

---

### 3. `StreamStats`

**Line**: 65  
**Methods**: 1

Statistics for a stream.

[TIP] **Suggested split**: Move to `streamstats.py`

---

### 4. `PooledStream`

**Line**: 82  
**Methods**: 6

A CUDA stream managed by a pool.

Attributes:
    stream_id: Unique identifier
    priority: Stream priority
    state: Current state
    stream: Underlying CUDA stream

[TIP] **Suggested split**: Move to `pooledstream.py`

---

### 5. `PooledEvent`

**Line**: 146  
**Methods**: 5

A CUDA event managed by a pool.

Attributes:
    event_id: Unique identifier
    event: Underlying CUDA event

[TIP] **Suggested split**: Move to `pooledevent.py`

---

### 6. `EventPool`

**Line**: 186  
**Methods**: 6

Pool of reusable CUDA events.

Events are expensive to create, so pooling them improves performance.

[TIP] **Suggested split**: Move to `eventpool.py`

---

### 7. `CudaStreamPool`

**Line**: 263  
**Methods**: 19

Pool of CUDA streams for compute and communication.

This pool manages separate stream pools for different operation
types, enabling efficient overlap of compute with data transfers.

Attributes:
    ...

[TIP] **Suggested split**: Move to `cudastreampool.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
