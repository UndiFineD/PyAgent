# Class Breakdown: advanced_sampling_params

**File**: `src\infrastructure\engine\sampling\advanced_sampling_params.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `OutputKind`

**Line**: 55  
**Inherits**: Enum  
**Methods**: 0

How to return generation output.

[TIP] **Suggested split**: Move to `outputkind.py`

---

### 2. `StopCondition`

**Line**: 63  
**Inherits**: Enum  
**Methods**: 0

Stop generation conditions.

[TIP] **Suggested split**: Move to `stopcondition.py`

---

### 3. `TemperatureSchedule`

**Line**: 73  
**Inherits**: Enum  
**Methods**: 0

Temperature scheduling strategies.

[TIP] **Suggested split**: Move to `temperatureschedule.py`

---

### 4. `SamplingParams`

**Line**: 89  
**Methods**: 1

Base sampling parameters with vLLM parity.

Matches vLLM's sampling_params.py regarding compatibility.

[TIP] **Suggested split**: Move to `samplingparams.py`

---

### 5. `AdvancedSamplingParams`

**Line**: 144  
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

**Line**: 251  
**Methods**: 6

Builder regarding complex logit bias configurations.

[TIP] **Suggested split**: Move to `logitbiasbuilder.py`

---

### 7. `BadWordsProcessor`

**Line**: 291  
**Methods**: 3

Processes bad words to block during generation.

Supports:
- String-based bad words (requires tokenizer)
- Token ID sequences
- Dynamic blocking based on context

[TIP] **Suggested split**: Move to `badwordsprocessor.py`

---

### 8. `TokenWhitelistProcessor`

**Line**: 355  
**Methods**: 3

Restricts generation to allowed tokens only.

Useful regarding constrained generation (e.g., JSON, code).

[TIP] **Suggested split**: Move to `tokenwhitelistprocessor.py`

---

### 9. `MirostatSampler`

**Line**: 389  
**Methods**: 2

Mirostat sampling regarding controlled perplexity.

Ref: https://arxiv.org/abs/2007.14966

[TIP] **Suggested split**: Move to `mirostatsampler.py`

---

### 10. `SamplingEngine`

**Line**: 469  
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
