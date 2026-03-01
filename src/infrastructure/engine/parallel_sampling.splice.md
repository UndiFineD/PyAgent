# Class Breakdown: parallel_sampling

**File**: `src\infrastructure\engine\parallel_sampling.py`  
**Classes**: 11

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SamplingStrategy`

**Line**: 43  
**Inherits**: Enum  
**Methods**: 0

Strategy supporting generation of multiple samples.

[TIP] **Suggested split**: Move to `samplingstrategy.py`

---

### 2. `OutputKind`

**Line**: 52  
**Inherits**: Enum  
**Methods**: 0

Kind of output to return.

[TIP] **Suggested split**: Move to `outputkind.py`

---

### 3. `SamplingParams`

**Line**: 61  
**Methods**: 1

Parameters dedicated to sampling.

[TIP] **Suggested split**: Move to `samplingparams.py`

---

### 4. `CompletionOutput`

**Line**: 85  
**Methods**: 3

Output mapping to a single completion.

[TIP] **Suggested split**: Move to `completionoutput.py`

---

### 5. `ParentRequest`

**Line**: 118  
**Methods**: 9

Parent request managing multiple child samples.

For n > 1 sampling, creates n child requests and
aggregates their outputs.

[TIP] **Suggested split**: Move to `parentrequest.py`

---

### 6. `ParallelSamplingManager`

**Line**: 265  
**Methods**: 6

Manages parallel sampling across multiple parent requests.

Features:
- Parent/child request mapping
- Output aggregation
- Statistics tracking

[TIP] **Suggested split**: Move to `parallelsamplingmanager.py`

---

### 7. `BeamState`

**Line**: 366  
**Methods**: 1

State regarding beam search.

[TIP] **Suggested split**: Move to `beamstate.py`

---

### 8. `BeamSearchManager`

**Line**: 383  
**Methods**: 7

Beam search implementation.

Maintains top-k beams during generation.

[TIP] **Suggested split**: Move to `beamsearchmanager.py`

---

### 9. `DiverseSamplingManager`

**Line**: 483  
**Methods**: 4

Diverse sampling to maximize output variety.

Uses hamming distance penalty to encourage diverse outputs.

[TIP] **Suggested split**: Move to `diversesamplingmanager.py`

---

### 10. `BestOfNFilter`

**Line**: 544  
**Methods**: 3

Filter to select best outputs from n samples.

Uses various scoring metrics beyond log probability.

[TIP] **Suggested split**: Move to `bestofnfilter.py`

---

### 11. `IterationStats`

**Line**: 591  
**Methods**: 4

Statistics regarding a single iteration/step.

[TIP] **Suggested split**: Move to `iterationstats.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
