# Class Breakdown: Params

**File**: `src\infrastructure\sampling\Params.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SamplingParams`

**Line**: 13  
**Methods**: 5

Parameters for controlling text generation sampling.

Attributes:
    temperature: Temperature for softmax. Higher = more random.
    top_k: Number of top tokens to consider. -1 or 0 = disabled.
    t...

[TIP] **Suggested split**: Move to `samplingparams.py`

---

### 2. `SamplingState`

**Line**: 79  
**Methods**: 4

Per-request state for sampling.

Tracks generated tokens and other stateful information needed
for penalties and constraints.

Attributes:
    request_id: Unique request identifier
    generated_ids: ...

[TIP] **Suggested split**: Move to `samplingstate.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
