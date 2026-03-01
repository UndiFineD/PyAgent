# Class Breakdown: AdvancedSamplingParams

**File**: `src\infrastructure\sampling\AdvancedSamplingParams.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `OutputKind`

**Line**: 30  
**Inherits**: Enum  
**Methods**: 0

How to return generation output.

[TIP] **Suggested split**: Move to `outputkind.py`

---

### 2. `StopCondition`

**Line**: 37  
**Inherits**: Enum  
**Methods**: 0

Stop generation conditions.

[TIP] **Suggested split**: Move to `stopcondition.py`

---

### 3. `TemperatureSchedule`

**Line**: 46  
**Inherits**: Enum  
**Methods**: 0

Temperature scheduling strategies.

[TIP] **Suggested split**: Move to `temperatureschedule.py`

---

### 4. `SamplingParams`

**Line**: 60  
**Methods**: 1

Base sampling parameters with vLLM parity.

Matches vLLM's sampling_params.py for compatibility.

[TIP] **Suggested split**: Move to `samplingparams.py`

---

### 5. `AdvancedSamplingParams`

**Line**: 114  
**Inherits**: SamplingParams  
**Methods**: 3

Extended sampling parameters beyond vLLM.

Features:
- Bad words blocking
- Flat logprobs format
- Allowed token whitelist
- Dynamic temperature scheduling
- Adaptive sampling based on entropy
- Conte...

[TIP] **Suggested split**: Move to `advancedsamplingparams.py`

---

### 6. `LogitBiasBuilder`

**Line**: 220  
**Methods**: 6

Builder for complex logit bias configurations.

[TIP] **Suggested split**: Move to `logitbiasbuilder.py`

---

### 7. `BadWordsProcessor`

**Line**: 256  
**Methods**: 3

Processes bad words to block during generation.

Supports:
- String-based bad words (requires tokenizer)
- Token ID sequences
- Dynamic blocking based on context

[TIP] **Suggested split**: Move to `badwordsprocessor.py`

---

### 8. `TokenWhitelistProcessor`

**Line**: 317  
**Methods**: 3

Restricts generation to allowed tokens only.

Useful for constrained generation (e.g., JSON, code).

[TIP] **Suggested split**: Move to `tokenwhitelistprocessor.py`

---

### 9. `MirostatSampler`

**Line**: 352  
**Methods**: 2

Mirostat sampling for controlled perplexity.

Ref: https://arxiv.org/abs/2007.14966

[TIP] **Suggested split**: Move to `mirostatsampler.py`

---

### 10. `SamplingEngine`

**Line**: 426  
**Methods**: 3

Unified sampling engine with all advanced features.

Combines:
- Temperature/top-k/top-p sampling
- Bad words blocking
- Token whitelisting
- Mirostat sampling
- Adaptive sampling

[TIP] **Suggested split**: Move to `samplingengine.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
