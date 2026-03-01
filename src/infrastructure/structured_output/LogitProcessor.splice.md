# Class Breakdown: LogitProcessor

**File**: `src\infrastructure\structured_output\LogitProcessor.py`  
**Classes**: 11

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LogitBias`

**Line**: 28  
**Methods**: 1

Logit bias specification for token manipulation.

Supports:
- Additive bias
- Multiplicative scaling
- Hard constraints (force/ban)

[TIP] **Suggested split**: Move to `logitbias.py`

---

### 2. `ProcessorStats`

**Line**: 53  
**Methods**: 1

Statistics for logit processors.

[TIP] **Suggested split**: Move to `processorstats.py`

---

### 3. `LogitProcessor`

**Line**: 71  
**Inherits**: ABC  
**Methods**: 7

Abstract base class for logit processors.

Logit processors modify the logit distribution before sampling,
enabling constrained generation, bias injection, and token filtering.

[TIP] **Suggested split**: Move to `logitprocessor.py`

---

### 4. `ConstrainedLogitProcessor`

**Line**: 132  
**Inherits**: LogitProcessor  
**Methods**: 2

Logit processor for constrained generation.

Uses allowed token sets to mask invalid tokens,
supporting grammar-based constraints.

[TIP] **Suggested split**: Move to `constrainedlogitprocessor.py`

---

### 5. `BitmaskLogitProcessor`

**Line**: 199  
**Inherits**: LogitProcessor  
**Methods**: 4

High-performance logit processor using pre-computed bitmasks.

Optimized for batch processing with vectorized operations.

[TIP] **Suggested split**: Move to `bitmasklogitprocessor.py`

---

### 6. `BiasLogitProcessor`

**Line**: 289  
**Inherits**: LogitProcessor  
**Methods**: 8

Logit processor for applying token biases.

Supports additive bias, scaling, and hard constraints.

[TIP] **Suggested split**: Move to `biaslogitprocessor.py`

---

### 7. `CompositeLogitProcessor`

**Line**: 379  
**Inherits**: LogitProcessor  
**Methods**: 9

Combines multiple logit processors.

Processors are applied in order, allowing complex constraint combinations.

[TIP] **Suggested split**: Move to `compositelogitprocessor.py`

---

### 8. `TemperatureProcessor`

**Line**: 450  
**Inherits**: LogitProcessor  
**Methods**: 3

Apply temperature scaling to logits.

[TIP] **Suggested split**: Move to `temperatureprocessor.py`

---

### 9. `TopKProcessor`

**Line**: 471  
**Inherits**: LogitProcessor  
**Methods**: 3

Apply top-k filtering to logits.

[TIP] **Suggested split**: Move to `topkprocessor.py`

---

### 10. `TopPProcessor`

**Line**: 504  
**Inherits**: LogitProcessor  
**Methods**: 3

Apply top-p (nucleus) filtering to logits.

[TIP] **Suggested split**: Move to `toppprocessor.py`

---

### 11. `RepetitionPenaltyProcessor`

**Line**: 546  
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
