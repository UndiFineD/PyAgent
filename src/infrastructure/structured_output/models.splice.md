# Class Breakdown: models

**File**: `src\infrastructure\structured_output\models.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `FSMState`

**Line**: 15  
**Methods**: 2

Immutable representation of FSM state.

[TIP] **Suggested split**: Move to `fsmstate.py`

---

### 2. `FSMTransitionTable`

**Line**: 35  
**Methods**: 5

Transition table for efficient FSM execution.

[TIP] **Suggested split**: Move to `fsmtransitiontable.py`

---

### 3. `TokenMask`

**Line**: 81  
**Methods**: 8

Token-level constraint mask.

[TIP] **Suggested split**: Move to `tokenmask.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
