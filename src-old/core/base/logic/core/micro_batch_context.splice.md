# Class Breakdown: micro_batch_context

**File**: `src\core\base\logic\core\micro_batch_context.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StreamType`

**Line**: 67  
**Inherits**: Enum  
**Methods**: 0

Type of CUDA stream.

[TIP] **Suggested split**: Move to `streamtype.py`

---

### 2. `MicroBatchState`

**Line**: 76  
**Inherits**: Enum  
**Methods**: 0

State of a micro-batch.

[TIP] **Suggested split**: Move to `microbatchstate.py`

---

### 3. `StreamHandle`

**Line**: 86  
**Methods**: 3

Handle to a CUDA stream with metadata.

[TIP] **Suggested split**: Move to `streamhandle.py`

---

### 4. `MicroBatchInfo`

**Line**: 118  
**Methods**: 1

Information about a single micro-batch.

[TIP] **Suggested split**: Move to `microbatchinfo.py`

---

### 5. `StreamManager`

**Line**: 139  
**Methods**: 7

Manages CUDA streams regarding compute and communication.

This class maintains separate stream pools regarding compute and
communication operations, enabling overlap of transfers with compute.

[TIP] **Suggested split**: Move to `streammanager.py`

---

### 6. `MicroBatchContext`

**Line**: 246  
**Inherits**: Unknown  
**Methods**: 12

Thread-synchronized micro-batch context.

This context manager handles the orchestration of micro-batches
with proper CUDA stream synchronization and thread barriers.

Attributes:
    batch_size: Tota...

[TIP] **Suggested split**: Move to `microbatchcontext.py`

---

### 7. `AdaptiveMicroBatchContext`

**Line**: 430  
**Inherits**: Unknown  
**Methods**: 3

Micro-batch context with adaptive sizing.

This extends MicroBatchContext to dynamically adjust micro-batch
sizes based on memory pressure and execution times.

[TIP] **Suggested split**: Move to `adaptivemicrobatchcontext.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
