# Class Breakdown: config

**File**: `src\infrastructure\logprobs\processor\config.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LogprobFormat`

**Line**: 7  
**Inherits**: Enum  
**Methods**: 0

Logprobs output format.

[TIP] **Suggested split**: Move to `logprobformat.py`

---

### 2. `TopLogprob`

**Line**: 15  
**Methods**: 2

Top-k logprob entry for a single token.

[TIP] **Suggested split**: Move to `toplogprob.py`

---

### 3. `LogprobEntry`

**Line**: 29  
**Methods**: 2

Logprob entry for a generated token.

[TIP] **Suggested split**: Move to `logprobentry.py`

---

### 4. `PromptLogprobs`

**Line**: 58  
**Methods**: 5

Logprobs for prompt tokens.

[TIP] **Suggested split**: Move to `promptlogprobs.py`

---

### 5. `SampleLogprobs`

**Line**: 82  
**Methods**: 9

Logprobs for sampled tokens.

[TIP] **Suggested split**: Move to `samplelogprobs.py`

---

### 6. `LogprobsResult`

**Line**: 121  
**Methods**: 2

Complete logprobs result.

[TIP] **Suggested split**: Move to `logprobsresult.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
