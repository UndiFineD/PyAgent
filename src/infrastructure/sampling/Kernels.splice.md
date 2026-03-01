# Class Breakdown: Kernels

**File**: `src\infrastructure\sampling\Kernels.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TemperatureSampler`

**Line**: 24  
**Inherits**: Sampler  
**Methods**: 1

Temperature scaling sampler.

[TIP] **Suggested split**: Move to `temperaturesampler.py`

---

### 2. `TopKSampler`

**Line**: 42  
**Inherits**: Sampler  
**Methods**: 1

Top-K filtering sampler.

[TIP] **Suggested split**: Move to `topksampler.py`

---

### 3. `TopPSampler`

**Line**: 62  
**Inherits**: Sampler  
**Methods**: 1

Top-P (nucleus) sampling.

[TIP] **Suggested split**: Move to `toppsampler.py`

---

### 4. `TopKTopPSampler`

**Line**: 94  
**Inherits**: Sampler  
**Methods**: 1

Combined top-k and top-p filtering.

[TIP] **Suggested split**: Move to `topktoppsampler.py`

---

### 5. `GumbelSampler`

**Line**: 140  
**Inherits**: Sampler  
**Methods**: 2

Gumbel-max trick sampler.

[TIP] **Suggested split**: Move to `gumbelsampler.py`

---

### 6. `RepetitionPenaltySampler`

**Line**: 171  
**Inherits**: Sampler  
**Methods**: 1

Repetition penalty sampler.

[TIP] **Suggested split**: Move to `repetitionpenaltysampler.py`

---

### 7. `PenaltySampler`

**Line**: 194  
**Inherits**: Sampler  
**Methods**: 1

Presence and frequency penalty sampler.

[TIP] **Suggested split**: Move to `penaltysampler.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
