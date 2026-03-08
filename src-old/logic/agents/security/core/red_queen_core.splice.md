# Class Breakdown: red_queen_core

**File**: `src\logic\agents\security\core\red_queen_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AttackVector`

**Line**: 33  
**Methods**: 0

Represents a simulated adversarial pattern for stress-testing guardrails.

[TIP] **Suggested split**: Move to `attackvector.py`

---

### 2. `RedQueenCore`

**Line**: 41  
**Methods**: 3

Pure logic for the 'Digital Red Queen' adversarial evolution.
Generates and mutates prompts to test security guardrails.

[TIP] **Suggested split**: Move to `redqueencore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
