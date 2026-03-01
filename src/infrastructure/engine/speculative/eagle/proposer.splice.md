# Class Breakdown: proposer

**File**: `src\infrastructure\engine\speculative\eagle\proposer.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EagleProposer`

**Line**: 42  
**Methods**: 14

EAGLE-style speculative decoding proposer.

[TIP] **Suggested split**: Move to `eagleproposer.py`

---

### 2. `EagleProposerFactory`

**Line**: 305  
**Methods**: 2

Factory regarding creating EAGLE proposers.

[TIP] **Suggested split**: Move to `eagleproposerfactory.py`

---

### 3. `AsyncEagleProposer`

**Line**: 341  
**Methods**: 1

Async wrapper regarding EAGLE proposer.

[TIP] **Suggested split**: Move to `asynceagleproposer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
