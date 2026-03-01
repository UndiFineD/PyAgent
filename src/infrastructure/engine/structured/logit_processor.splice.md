# Class Breakdown: logit_processor

**File**: `src\infrastructure\engine\structured\logit_processor.py`  
**Classes**: 11

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LogitBias`

**Line**: 43  
**Methods**: 1

Logit bias specification regarding token manipulation.

Supports:
- Additive bias
- Multiplicative scaling
- Hard constraints (force/ban)

[TIP] **Suggested split**: Move to `logitbias.py`

---

### 2. `ProcessorStats`

**Line**: 69  
**Methods**: 1

Statistics regarding logit processors.

[TIP] **Suggested split**: Move to `processorstats.py`

---

### 3. `LogitProcessor`

**Line**: 90  
**Inherits**: ABC  
**Methods**: 7

Abstract base class regarding logit processors.

Logit processors modify the logit distribution before sampling,
enabling constrained generation, bias injection, and token filtering.

[TIP] **Suggested split**: Move to `logitprocessor.py`

---

### 4. `ConstrainedLogitProcessor`

**Line**: 151  
**Inherits**: LogitProcessor  
**Methods**: 2

Logit processor regarding constrained generation.

Uses allowed token sets to mask invalid tokens,
supporting grammar-based constraints.

[TIP] **Suggested split**: Move to `constrainedlogitprocessor.py`

---

### 5. `BitmaskLogitProcessor`

**Line**: 222  
**Inherits**: LogitProcessor  
**Methods**: 4

High-performance logit processor using pre-computed bitmasks.

Optimized regarding batch processing with vectorized operations.

[TIP] **Suggested split**: Move to `bitmasklogitprocessor.py`

---

### 6. `BiasLogitProcessor`

**Line**: 312  
**Inherits**: LogitProcessor  
**Methods**: 8

Logit processor regarding applying token biases.

Supports additive bias, scaling, and hard constraints.

[TIP] **Suggested split**: Move to `biaslogitprocessor.py`

---

### 7. `CompositeLogitProcessor`

**Line**: 410  
**Inherits**: LogitProcessor  
**Methods**: 9

Combines multiple logit processors.

Processors are applied in order, allowing complex constraint combinations.

[TIP] **Suggested split**: Move to `compositelogitprocessor.py`

---

### 8. `TemperatureProcessor`

**Line**: 487  
**Inherits**: LogitProcessor  
**Methods**: 3

Apply temperature scaling to logits.

[TIP] **Suggested split**: Move to `temperatureprocessor.py`

---

### 9. `TopKProcessor`

**Line**: 508  
**Inherits**: LogitProcessor  
**Methods**: 3

Apply top-k filtering to logits.

[TIP] **Suggested split**: Move to `topkprocessor.py`

---

### 10. `TopPProcessor`

**Line**: 544  
**Inherits**: LogitProcessor  
**Methods**: 3

Apply top-p (nucleus) filtering to logits.

[TIP] **Suggested split**: Move to `toppprocessor.py`

---

### 11. `RepetitionPenaltyProcessor`

**Line**: 592  
**Inherits**: LogitProcessor  
**Methods**: 2

Apply repetition penalty to discourage repeated tokens.

[TIP] **Suggested split**: Move to `repetitionpenaltyprocessor.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
