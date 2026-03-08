# Class Breakdown: RewardFunctions

**File**: `src\core\rl\RewardFunctions.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RewardType`

**Line**: 10  
**Inherits**: Enum  
**Methods**: 0

[TIP] **Suggested split**: Move to `rewardtype.py`

---

### 2. `RewardSignal`

**Line**: 17  
**Methods**: 0

Structured reward with metadata.

[TIP] **Suggested split**: Move to `rewardsignal.py`

---

### 3. `RewardFunctions`

**Line**: 24  
**Methods**: 8

Library of standard reward functions for agentic behavior.

[TIP] **Suggested split**: Move to `rewardfunctions.py`

---

### 4. `CompositeRewardFunction`

**Line**: 91  
**Methods**: 3

Combines multiple reward functions with weights.

[TIP] **Suggested split**: Move to `compositerewardfunction.py`

---

### 5. `RewardShaper`

**Line**: 114  
**Methods**: 2

Applies potential-based reward shaping to avoid changing optimal policy.

[TIP] **Suggested split**: Move to `rewardshaper.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
