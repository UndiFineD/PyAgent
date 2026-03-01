# Class Breakdown: engine

**File**: `src\infrastructure\logprobs\processor\engine.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LogprobsProcessor`

**Line**: 9  
**Methods**: 4

Process and extract logprobs from model outputs.

[TIP] **Suggested split**: Move to `logprobsprocessor.py`

---

### 2. `StreamingLogprobs`

**Line**: 46  
**Methods**: 3

Streaming logprobs accumulator.

[TIP] **Suggested split**: Move to `streaminglogprobs.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
