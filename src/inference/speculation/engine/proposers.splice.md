# Class Breakdown: proposers

**File**: `src\inference\speculation\engine\proposers.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `NgramProposer`

**Line**: 56  
**Inherits**: DrafterBase  
**Methods**: 9

N-gram based draft token proposer.

[TIP] **Suggested split**: Move to `ngramproposer.py`

---

### 2. `SuffixProposer`

**Line**: 235  
**Inherits**: DrafterBase  
**Methods**: 4

Suffix-based draft token proposer.

[TIP] **Suggested split**: Move to `suffixproposer.py`

---

### 3. `EagleProposer`

**Line**: 320  
**Inherits**: DrafterBase  
**Methods**: 4

EAGLE tree-based draft token proposer.

[TIP] **Suggested split**: Move to `eagleproposer.py`

---

### 4. `HybridDrafter`

**Line**: 399  
**Inherits**: DrafterBase  
**Methods**: 3

Hybrid drafter combining multiple speculation methods.

[TIP] **Suggested split**: Move to `hybriddrafter.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
