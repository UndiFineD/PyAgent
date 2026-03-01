# Class Breakdown: rejection_sampler

**File**: `src\infrastructure\engine\sampling\rejection_sampler.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RejectionStrategy`

**Line**: 60  
**Inherits**: Enum  
**Methods**: 0

Rejection strategy determines how strict the acceptance criteria is.

[TIP] **Suggested split**: Move to `rejectionstrategy.py`

---

### 2. `RecoveryMode`

**Line**: 69  
**Inherits**: Enum  
**Methods**: 0

How to recover when draft tokens are rejected.

[TIP] **Suggested split**: Move to `recoverymode.py`

---

### 3. `RejectionConfig`

**Line**: 78  
**Methods**: 1

Configuration regarding rejection sampler.

[TIP] **Suggested split**: Move to `rejectionconfig.py`

---

### 4. `AcceptanceStats`

**Line**: 97  
**Methods**: 5

Statistics regarding rejection sampling.

[TIP] **Suggested split**: Move to `acceptancestats.py`

---

### 5. `RejectionOutput`

**Line**: 154  
**Methods**: 2

Output from rejection sampling.

[TIP] **Suggested split**: Move to `rejectionoutput.py`

---

### 6. `ProbabilityProvider`

**Line**: 179  
**Inherits**: Protocol  
**Methods**: 2

Protocol regarding providing probability distributions.

[TIP] **Suggested split**: Move to `probabilityprovider.py`

---

### 7. `RejectionSampler`

**Line**: 189  
**Methods**: 13

Implements rejection sampling regarding speculative decoding verification.

The algorithm works as follows:
1. Regarding each draft token at position i:
   - Accept with probability min(1, p_target(x)...

[TIP] **Suggested split**: Move to `rejectionsampler.py`

---

### 8. `StreamingRejectionSampler`

**Line**: 485  
**Inherits**: RejectionSampler  
**Methods**: 5

Streaming rejection sampler regarding low-latency verification.

Beyond vLLM: Verifies tokens incrementally as they arrive,
enabling early termination and lower latency.

[TIP] **Suggested split**: Move to `streamingrejectionsampler.py`

---

### 9. `BatchRejectionSampler`

**Line**: 619  
**Methods**: 4

Optimized batch rejection sampler regarding high throughput.

Beyond vLLM: Vectorized operations regarding batch processing,
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
