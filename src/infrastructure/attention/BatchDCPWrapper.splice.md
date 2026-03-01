# Class Breakdown: BatchDCPWrapper

**File**: `src\infrastructure\attention\BatchDCPWrapper.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BatchPhase`

**Line**: 59  
**Inherits**: Enum  
**Methods**: 0

Phase of batch processing.

[TIP] **Suggested split**: Move to `batchphase.py`

---

### 2. `AllReduceStrategy`

**Line**: 66  
**Inherits**: Enum  
**Methods**: 0

Strategy for distributed reduction.

[TIP] **Suggested split**: Move to `allreducestrategy.py`

---

### 3. `BatchRequest`

**Line**: 75  
**Methods**: 0

A request in a batch.

Tracks per-request state within a batch.

[TIP] **Suggested split**: Move to `batchrequest.py`

---

### 4. `BatchMetadata`

**Line**: 99  
**Methods**: 2

Metadata for a batch of requests.

Inspired by vLLM's batch metadata structures.

[TIP] **Suggested split**: Move to `batchmetadata.py`

---

### 5. `DCPPlanConfig`

**Line**: 137  
**Methods**: 0

Configuration for DCP planning.

Controls how batches are planned and executed.

[TIP] **Suggested split**: Move to `dcpplanconfig.py`

---

### 6. `ExecutionPlan`

**Line**: 167  
**Methods**: 0

Plan for executing a batch.

Produced by plan() method, consumed by run() method.

[TIP] **Suggested split**: Move to `executionplan.py`

---

### 7. `BatchExecutor`

**Line**: 194  
**Inherits**: ABC  
**Methods**: 2

Abstract base for batch execution.

[TIP] **Suggested split**: Move to `batchexecutor.py`

---

### 8. `BatchDCPPrefillWrapper`

**Line**: 227  
**Inherits**: BatchExecutor  
**Methods**: 4

Wrapper for batch DCP prefill operations.

Coordinates prefill across a batch of requests,
preparing KV cache for transfer to decode instances.

Inspired by vLLM's BatchDCPPrefillWrapper pattern.

[TIP] **Suggested split**: Move to `batchdcpprefillwrapper.py`

---

### 9. `BatchDCPDecodeWrapper`

**Line**: 373  
**Inherits**: BatchExecutor  
**Methods**: 6

Wrapper for batch DCP decode operations.

Coordinates decode across a batch of requests that
receive KV cache from prefill instances.

[TIP] **Suggested split**: Move to `batchdcpdecodewrapper.py`

---

### 10. `UnifiedBatchWrapper`

**Line**: 537  
**Methods**: 3

Unified wrapper for mixed prefill/decode batches.

Beyond vLLM: Single interface for heterogeneous batches.

[TIP] **Suggested split**: Move to `unifiedbatchwrapper.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
