# Class Breakdown: BeamSearch

**File**: `src\infrastructure\sampling\BeamSearch.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BeamSearchConfig`

**Line**: 21  
**Methods**: 0

Configuration for beam search.

[TIP] **Suggested split**: Move to `beamsearchconfig.py`

---

### 2. `BeamHypothesis`

**Line**: 30  
**Methods**: 4

A hypothesis in beam search.

[TIP] **Suggested split**: Move to `beamhypothesis.py`

---

### 3. `BeamSearchSampler`

**Line**: 60  
**Inherits**: Sampler  
**Methods**: 6

Beam search sampler.

[TIP] **Suggested split**: Move to `beamsearchsampler.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
