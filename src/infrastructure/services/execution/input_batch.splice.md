# Class Breakdown: input_batch

**File**: `src\infrastructure\services\execution\input_batch.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SamplingMetadata`

**Line**: 37  
**Methods**: 4

Per-request sampling parameters for batched sampling.

Based on vLLM's SamplingMetadata pattern.

[TIP] **Suggested split**: Move to `samplingmetadata.py`

---

### 2. `InputBuffers`

**Line**: 144  
**Methods**: 2

Pre-allocated tensors for batch inputs.

Avoids runtime allocation during model execution.
Based on vLLM's InputBuffers pattern.

[TIP] **Suggested split**: Move to `inputbuffers.py`

---

### 3. `InputBatch`

**Line**: 222  
**Methods**: 8

Structured batch for model execution.

Contains all inputs and metadata needed for a forward pass.
Based on vLLM's InputBatch pattern.

[TIP] **Suggested split**: Move to `inputbatch.py`

---

### 4. `BatchBuilder`

**Line**: 401  
**Methods**: 8

Builder for constructing InputBatch instances.

Accumulates requests and builds batches efficiently.

[TIP] **Suggested split**: Move to `batchbuilder.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
