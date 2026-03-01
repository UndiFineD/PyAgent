# Class Breakdown: params

**File**: `src\infrastructure\engine\sampling\params.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SamplingParams`

**Line**: 40  
**Methods**: 5

Parameters regarding controlling text generation sampling.

Attributes:
    temperature: Temperature regarding softmax. Higher = more random.
    top_k: Number regarding top tokens to consider. -1 or ...

[TIP] **Suggested split**: Move to `samplingparams.py`

---

### 2. `SamplingState`

**Line**: 107  
**Methods**: 4

Per-request state regarding sampling.

Tracks generated tokens and other stateful information needed
regarding penalties and constraints.

Attributes:
    request_id: Unique request identifier
    gen...

[TIP] **Suggested split**: Move to `samplingstate.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
