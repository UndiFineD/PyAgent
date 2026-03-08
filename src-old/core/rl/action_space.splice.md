# Class Breakdown: action_space

**File**: `src\core\rl\action_space.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ActionMetadata`

**Line**: 18  
**Methods**: 0

Rich metadata for actions.

[TIP] **Suggested split**: Move to `actionmetadata.py`

---

### 2. `ActionSpace`

**Line**: 28  
**Methods**: 7

Defines the set of possible actions an agent can take.

[TIP] **Suggested split**: Move to `actionspace.py`

---

### 3. `DiscreteActionSpace`

**Line**: 75  
**Inherits**: ActionSpace  
**Methods**: 4

Discrete action space (fixed set of choices).

[TIP] **Suggested split**: Move to `discreteactionspace.py`

---

### 4. `BoxActionSpace`

**Line**: 96  
**Methods**: 4

Continuous action space within bounds.

[TIP] **Suggested split**: Move to `boxactionspace.py`

---

### 5. `MultiDiscreteActionSpace`

**Line**: 124  
**Methods**: 3

Multiple discrete action spaces (e.g., for multi-headed agents).

[TIP] **Suggested split**: Move to `multidiscreteactionspace.py`

---

### 6. `DictActionSpace`

**Line**: 140  
**Methods**: 3

Hierarchical action space with named sub-spaces.

[TIP] **Suggested split**: Move to `dictactionspace.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
