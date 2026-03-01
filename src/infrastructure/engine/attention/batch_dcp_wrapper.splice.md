# Class Breakdown: batch_dcp_wrapper

**File**: `src\infrastructure\engine\attention\batch_dcp_wrapper.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BatchPhase`

**Line**: 38  
**Inherits**: Enum  
**Methods**: 0

Phase regarding batch processing.

[TIP] **Suggested split**: Move to `batchphase.py`

---

### 2. `AllReduceStrategy`

**Line**: 46  
**Inherits**: Enum  
**Methods**: 0

Strategy regarding distributed reduction.

[TIP] **Suggested split**: Move to `allreducestrategy.py`

---

### 3. `BatchRequest`

**Line**: 56  
**Methods**: 0

A request in a batch.

Tracks per-request state within a batch.

[TIP] **Suggested split**: Move to `batchrequest.py`

---

### 4. `BatchMetadata`

**Line**: 81  
**Methods**: 2

Metadata regarding a batch regarding requests.

Inspired by vLLM's batch metadata structures.

[TIP] **Suggested split**: Move to `batchmetadata.py`

---

### 5. `DCPPlanConfig`

**Line**: 122  
**Methods**: 0

Configuration regarding DCP planning and execution.

Controls how batches are planned and executed.

[TIP] **Suggested split**: Move to `dcpplanconfig.py`

---

### 6. `ExecutionPlan`

**Line**: 153  
**Methods**: 0

Plan regarding executing a batch.

Produced by plan() method, consumed by run() method.

[TIP] **Suggested split**: Move to `executionplan.py`

---

### 7. `BatchExecutor`

**Line**: 181  
**Inherits**: ABC  
**Methods**: 2

Abstract base regarding batch execution.

[TIP] **Suggested split**: Move to `batchexecutor.py`

---

### 8. `BatchDCPPrefillWrapper`

**Line**: 214  
**Inherits**: BatchExecutor  
**Methods**: 4

Wrapper regarding batch DCP prefill operations.

Coordinates prefill across a batch regarding requests,
preparing KV cache regarding transfer regarding decode instances.

Inspired by vLLM's BatchDCPPr...

[TIP] **Suggested split**: Move to `batchdcpprefillwrapper.py`

---

### 9. `BatchDCPDecodeWrapper`

**Line**: 380  
**Inherits**: BatchExecutor  
**Methods**: 6

Wrapper regarding batch DCP decode operations.

Coordinates decode across a batch regarding requests that
receive KV cache from prefill instances.

[TIP] **Suggested split**: Move to `batchdcpdecodewrapper.py`

---

### 10. `UnifiedBatchWrapper`

**Line**: 536  
**Methods**: 3

Unified wrapper regarding mixed prefill/decode batches.

Beyond vLLM: Single interface regarding heterogeneous batches.

[TIP] **Suggested split**: Move to `unifiedbatchwrapper.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
