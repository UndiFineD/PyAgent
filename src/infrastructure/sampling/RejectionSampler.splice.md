# Class Breakdown: RejectionSampler

**File**: `src\infrastructure\sampling\RejectionSampler.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RejectionStrategy`

**Line**: 40  
**Inherits**: Enum  
**Methods**: 0

Rejection strategy determines how strict the acceptance criteria is.

[TIP] **Suggested split**: Move to `rejectionstrategy.py`

---

### 2. `RecoveryMode`

**Line**: 48  
**Inherits**: Enum  
**Methods**: 0

How to recover when draft tokens are rejected.

[TIP] **Suggested split**: Move to `recoverymode.py`

---

### 3. `RejectionConfig`

**Line**: 56  
**Methods**: 1

Configuration for rejection sampler.

[TIP] **Suggested split**: Move to `rejectionconfig.py`

---

### 4. `AcceptanceStats`

**Line**: 74  
**Methods**: 5

Statistics for rejection sampling.

[TIP] **Suggested split**: Move to `acceptancestats.py`

---

### 5. `RejectionOutput`

**Line**: 125  
**Methods**: 2

Output from rejection sampling.

[TIP] **Suggested split**: Move to `rejectionoutput.py`

---

### 6. `ProbabilityProvider`

**Line**: 149  
**Inherits**: Protocol  
**Methods**: 2

Protocol for providing probability distributions.

[TIP] **Suggested split**: Move to `probabilityprovider.py`

---

### 7. `RejectionSampler`

**Line**: 161  
**Methods**: 11

Implements rejection sampling for speculative decoding verification.

The algorithm works as follows:
1. For each draft token at position i:
   - Accept with probability min(1, p_target(x) / p_draft(x...

[TIP] **Suggested split**: Move to `rejectionsampler.py`

---

### 8. `StreamingRejectionSampler`

**Line**: 406  
**Inherits**: RejectionSampler  
**Methods**: 4

Streaming rejection sampler for low-latency verification.

Beyond vLLM: Verifies tokens incrementally as they arrive,
enabling early termination and lower latency.

[TIP] **Suggested split**: Move to `streamingrejectionsampler.py`

---

### 9. `BatchRejectionSampler`

**Line**: 525  
**Methods**: 2

Optimized batch rejection sampler for high throughput.

Beyond vLLM: Vectorized operations for batch processing,
memory-efficient probability handling, parallel verification.

[TIP] **Suggested split**: Move to `batchrejectionsampler.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
