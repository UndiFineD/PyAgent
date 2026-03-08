# Class Breakdown: mdp

**File**: `src\core\rl\mdp.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `Transition`

**Line**: 20  
**Methods**: 0

Represents a state transition with optional metadata.

[TIP] **Suggested split**: Move to `transition.py`

---

### 2. `ExperienceReplayBuffer`

**Line**: 33  
**Methods**: 3

Circular buffer for storing and sampling transitions.

[TIP] **Suggested split**: Move to `experiencereplaybuffer.py`

---

### 3. `MDP`

**Line**: 61  
**Methods**: 9

Models the decision-making process for agents.
Implements: S (States), A (Actions), P(s'|s,a) (Transition Dynamics), R(s,a) (Rewards)
Enhanced with value iteration, policy extraction, and model-based ...

[TIP] **Suggested split**: Move to `mdp.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
