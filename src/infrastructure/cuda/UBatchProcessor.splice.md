# Class Breakdown: UBatchProcessor

**File**: `src\infrastructure\cuda\UBatchProcessor.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `UBatchState`

**Line**: 31  
**Inherits**: Enum  
**Methods**: 0

State of micro-batch processing.

[TIP] **Suggested split**: Move to `ubatchstate.py`

---

### 2. `UBatchSlice`

**Line**: 41  
**Methods**: 1

Describes a slice of the input batch for micro-batching.

Attributes:
    token_slice: Slice object for token range
    req_slice: Slice object for request range
    num_tokens: Number of tokens in sl...

[TIP] **Suggested split**: Move to `ubatchslice.py`

---

### 3. `UBatchContext`

**Line**: 74  
**Methods**: 3

Execution context for a micro-batch.

Attributes:
    slice_info: Slice describing this micro-batch
    thread_id: Thread handling this context
    cpu_wait_event: Event for CPU synchronization
    gp...

[TIP] **Suggested split**: Move to `ubatchcontext.py`

---

### 4. `UbatchMetadata`

**Line**: 103  
**Methods**: 0

Metadata for a micro-batch execution.

Attributes:
    context: Execution context
    input_ids: Sliced input token IDs
    positions: Sliced position IDs
    inputs_embeds: Optional sliced embeddings...

[TIP] **Suggested split**: Move to `ubatchmetadata.py`

---

### 5. `UBatchConfig`

**Line**: 124  
**Methods**: 0

Configuration for micro-batch processing.

[TIP] **Suggested split**: Move to `ubatchconfig.py`

---

### 6. `UBatchBarrier`

**Line**: 133  
**Methods**: 4

Barrier for synchronizing micro-batch threads.

Provides coordination between main thread and worker threads
during CUDA graph capture and execution.

[TIP] **Suggested split**: Move to `ubatchbarrier.py`

---

### 7. `UBatchWrapper`

**Line**: 183  
**Methods**: 11

Wraps a model to enable micro-batch execution.

Based on vLLM's UBatchWrapper for efficient CUDA graph usage
with data parallel workloads. Splits large batches into
micro-batches for better graph hit ...

[TIP] **Suggested split**: Move to `ubatchwrapper.py`

---

### 8. `DynamicUBatchWrapper`

**Line**: 457  
**Inherits**: UBatchWrapper  
**Methods**: 5

Extended wrapper with dynamic sizing based on memory.

Beyond vLLM:
- Adjusts ubatch count based on memory pressure
- Learns optimal sizing from history

[TIP] **Suggested split**: Move to `dynamicubatchwrapper.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
