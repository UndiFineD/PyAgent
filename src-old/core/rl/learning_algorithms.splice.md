# Class Breakdown: learning_algorithms

**File**: `src\core\rl\learning_algorithms.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PolicyGradientBuffer`

**Line**: 21  
**Methods**: 3

Stores trajectory data for policy gradient methods.

[TIP] **Suggested split**: Move to `policygradientbuffer.py`

---

### 2. `LearningAlgorithms`

**Line**: 58  
**Methods**: 7

Standard RL algorithms for agent policy improvement.

[TIP] **Suggested split**: Move to `learningalgorithms.py`

---

### 3. `PolicyOptimizer`

**Line**: 188  
**Methods**: 3

High-level policy optimization utilities.

[TIP] **Suggested split**: Move to `policyoptimizer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
