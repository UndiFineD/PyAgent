# Class Breakdown: cuda_stream_pool

**File**: `src\core\base\logic\core\cuda_stream_pool.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StreamPriority`

**Line**: 66  
**Inherits**: Enum  
**Methods**: 0

Priority level regarding CUDA streams.

[TIP] **Suggested split**: Move to `streampriority.py`

---

### 2. `StreamState`

**Line**: 74  
**Inherits**: Enum  
**Methods**: 0

State of a pooled stream.

[TIP] **Suggested split**: Move to `streamstate.py`

---

### 3. `StreamStats`

**Line**: 83  
**Methods**: 1

Statistics regarding a stream.

[TIP] **Suggested split**: Move to `streamstats.py`

---

### 4. `PooledStream`

**Line**: 101  
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

**Line**: 166  
**Methods**: 5

A CUDA event managed by a pool.

Attributes:
    event_id: Unique identifier
    event: Underlying CUDA event

[TIP] **Suggested split**: Move to `pooledevent.py`

---

### 6. `EventPool`

**Line**: 207  
**Methods**: 6

Pool of reusable CUDA events.

Events are expensive to create, so pooling them improves performance.

[TIP] **Suggested split**: Move to `eventpool.py`

---

### 7. `CudaStreamPool`

**Line**: 285  
**Methods**: 19

Pool of CUDA streams regarding compute and communication.

This pool manages separate stream pools regarding different operation
types, enabling efficient overlap of compute with data transfers.

Attr...

[TIP] **Suggested split**: Move to `cudastreampool.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
