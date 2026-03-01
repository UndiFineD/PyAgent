# Class Breakdown: LogitsProcessorV2

**File**: `src\infrastructure\structured_output\LogitsProcessorV2.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MoveDirectionality`

**Line**: 51  
**Inherits**: Enum  
**Methods**: 0

Direction of request movement within batch.

[TIP] **Suggested split**: Move to `movedirectionality.py`

---

### 2. `SamplingParams`

**Line**: 58  
**Methods**: 1

Sampling parameters for a request.

[TIP] **Suggested split**: Move to `samplingparams.py`

---

### 3. `BatchUpdate`

**Line**: 87  
**Methods**: 2

Batch state change information for logits processors.

Contains metadata for requests added to, removed from, and moved
within the persistent batch. Operations should be processed in order:
removed, a...

[TIP] **Suggested split**: Move to `batchupdate.py`

---

### 4. `BatchUpdateBuilder`

**Line**: 116  
**Methods**: 7

Builder for constructing BatchUpdate objects.

[TIP] **Suggested split**: Move to `batchupdatebuilder.py`

---

### 5. `LogitsProcessor`

**Line**: 178  
**Inherits**: ABC  
**Methods**: 6

Abstract base class for logits processors.

Processors modify logits before sampling to implement constraints
like temperature, top-k, min-p, bad words, etc.

[TIP] **Suggested split**: Move to `logitsprocessor.py`

---

### 6. `MinPLogitsProcessor`

**Line**: 238  
**Inherits**: LogitsProcessor  
**Methods**: 9

Min-P sampling logits processor.

Filters tokens with probability below (min_p * max_probability).
Does not affect greedy sampling (argmax invariant).

[TIP] **Suggested split**: Move to `minplogitsprocessor.py`

---

### 7. `LogitBiasLogitsProcessor`

**Line**: 361  
**Inherits**: LogitsProcessor  
**Methods**: 8

Logit bias processor.

Adds bias values to specific token logits. Can change argmax
results, so not argmax invariant.

[TIP] **Suggested split**: Move to `logitbiaslogitsprocessor.py`

---

### 8. `CompositeLogitsProcessor`

**Line**: 467  
**Inherits**: LogitsProcessor  
**Methods**: 8

Composite processor that chains multiple processors.

Beyond vLLM: Allows flexible composition of processors
with optimized execution order.

[TIP] **Suggested split**: Move to `compositelogitsprocessor.py`

---

### 9. `LogitsProcessorRegistry`

**Line**: 520  
**Methods**: 6

Registry for logits processor types.

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
