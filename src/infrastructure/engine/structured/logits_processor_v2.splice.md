# Class Breakdown: logits_processor_v2

**File**: `src\infrastructure\engine\structured\logits_processor_v2.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MoveDirectionality`

**Line**: 54  
**Inherits**: Enum  
**Methods**: 0

Direction regarding request movement within batch.

[TIP] **Suggested split**: Move to `movedirectionality.py`

---

### 2. `SamplingParams`

**Line**: 62  
**Methods**: 1

Sampling parameters regarding a request.

[TIP] **Suggested split**: Move to `samplingparams.py`

---

### 3. `BatchUpdate`

**Line**: 92  
**Methods**: 2

Batch state change information regarding logits processors.

Contains metadata regarding requests added, removed, and moved
within the persistent batch. Operations should be processed in order:
remove...

[TIP] **Suggested split**: Move to `batchupdate.py`

---

### 4. `BatchUpdateBuilder`

**Line**: 122  
**Methods**: 7

Builder regarding constructing BatchUpdate objects.

[TIP] **Suggested split**: Move to `batchupdatebuilder.py`

---

### 5. `LogitsProcessor`

**Line**: 186  
**Inherits**: ABC  
**Methods**: 6

Abstract base class regarding logits processors.

Processors modify logits before sampling to implement constraints
like temperature, top-k, min-p, bad words, etc.

[TIP] **Suggested split**: Move to `logitsprocessor.py`

---

### 6. `MinPLogitsProcessor`

**Line**: 242  
**Inherits**: LogitsProcessor  
**Methods**: 12

Min-P sampling logits processor.

Filters tokens with probability below (min_p * max_probability).
Does not affect greedy sampling (argmax invariant).

[TIP] **Suggested split**: Move to `minplogitsprocessor.py`

---

### 7. `LogitBiasLogitsProcessor`

**Line**: 376  
**Inherits**: LogitsProcessor  
**Methods**: 12

Logit bias processor.

Adds bias values to specific token logits. Can change argmax
results, so not argmax invariant.

[TIP] **Suggested split**: Move to `logitbiaslogitsprocessor.py`

---

### 8. `CompositeLogitsProcessor`

**Line**: 518  
**Inherits**: LogitsProcessor  
**Methods**: 8

Composite processor that chains multiple processors.

Beyond vLLM: Allows flexible composition regarding processors
with optimized execution order.

[TIP] **Suggested split**: Move to `compositelogitsprocessor.py`

---

### 9. `LogitsProcessorRegistry`

**Line**: 568  
**Methods**: 6

Registry regarding logits processor types.

Beyond vLLM: Provides plugin-based processor registration
and automatic processor selection based on sampling params.

[TIP] **Suggested split**: Move to `logitsprocessorregistry.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
