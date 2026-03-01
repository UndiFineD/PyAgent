# Class Breakdown: proposer

**File**: `src\infrastructure\sampling\ngram\proposer.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `NgramProposer`

**Line**: 31  
**Methods**: 9

N-gram based speculative token proposer.

Uses n-gram matching on prompt/context to propose
likely continuations without running a draft model.

[TIP] **Suggested split**: Move to `ngramproposer.py`

---

### 2. `AdaptiveNgramProposer`

**Line**: 229  
**Inherits**: NgramProposer  
**Methods**: 3

Adaptive n-gram proposer that adjusts parameters based on performance.

[TIP] **Suggested split**: Move to `adaptivengramproposer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
