# Class Breakdown: models

**File**: `src\infrastructure\services\execution\batch\models.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MoveDirectionality`

**Line**: 30  
**Inherits**: Enum  
**Methods**: 0

Direction of request movement in batch.

[TIP] **Suggested split**: Move to `movedirectionality.py`

---

### 2. `CachedRequestState`

**Line**: 38  
**Methods**: 1

Per-request state cache matching vLLM's CachedRequestState.

[TIP] **Suggested split**: Move to `cachedrequeststate.py`

---

### 3. `BatchUpdateBuilder`

**Line**: 77  
**Methods**: 4

Tracks request movements within a batch for logits processors.

[TIP] **Suggested split**: Move to `batchupdatebuilder.py`

---

### 4. `SamplingMetadata`

**Line**: 106  
**Methods**: 0

GPU-resident sampling parameters for a batch.

[TIP] **Suggested split**: Move to `samplingmetadata.py`

---

### 5. `InputBatch`

**Line**: 127  
**Methods**: 0

Complete batch representation for model execution.

[TIP] **Suggested split**: Move to `inputbatch.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
