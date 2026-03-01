# Class Breakdown: Proposer

**File**: `src\infrastructure\speculative_v2\eagle\Proposer.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EagleProposer`

**Line**: 25  
**Methods**: 12

EAGLE-style speculative decoding proposer.

[TIP] **Suggested split**: Move to `eagleproposer.py`

---

### 2. `EagleProposerFactory`

**Line**: 286  
**Methods**: 2

Factory for creating EAGLE proposers.

[TIP] **Suggested split**: Move to `eagleproposerfactory.py`

---

### 3. `AsyncEagleProposer`

**Line**: 325  
**Methods**: 1

Async wrapper for EAGLE proposer.

[TIP] **Suggested split**: Move to `asynceagleproposer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
