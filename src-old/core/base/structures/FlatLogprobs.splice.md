# Class Breakdown: FlatLogprobs

**File**: `src\core\base\structures\FlatLogprobs.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `Logprob`

**Line**: 18  
**Methods**: 0

Log probability information for a single token.

Attributes:
    logprob: The log probability of the token
    rank: The vocab rank of the token (1-based, or None)
    decoded_token: The decoded strin...

[TIP] **Suggested split**: Move to `logprob.py`

---

### 2. `FlatLogprobs`

**Line**: 37  
**Inherits**: Unknown  
**Methods**: 14

Memory-efficient flat storage for log probabilities.

Compared to list[dict[int, Logprob]], this data structure reduces GC
overhead significantly by flattening logprob information for all positions
an...

[TIP] **Suggested split**: Move to `flatlogprobs.py`

---

### 3. `LogprobsAccumulator`

**Line**: 264  
**Methods**: 6

Accumulator for building FlatLogprobs incrementally.

Provides a builder pattern for constructing logprobs
with validation and statistics.

[TIP] **Suggested split**: Move to `logprobsaccumulator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
