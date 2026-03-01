# Class Breakdown: proposers

**File**: `src\infrastructure\engine\speculative\decoder\proposers.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ProposerStats`

**Line**: 32  
**Methods**: 2

Statistics regarding a proposer.

[TIP] **Suggested split**: Move to `proposerstats.py`

---

### 2. `SpeculativeProposer`

**Line**: 55  
**Inherits**: ABC  
**Methods**: 5

Abstract base class regarding speculative token proposers.

[TIP] **Suggested split**: Move to `speculativeproposer.py`

---

### 3. `NgramProposer`

**Line**: 89  
**Inherits**: SpeculativeProposer  
**Methods**: 5

N-gram based speculative proposer.

[TIP] **Suggested split**: Move to `ngramproposer.py`

---

### 4. `MedusaProposer`

**Line**: 190  
**Inherits**: SpeculativeProposer  
**Methods**: 4

Medusa-style multi-head prediction proposer.

[TIP] **Suggested split**: Move to `medusaproposer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
