# Class Breakdown: LearningObjectives

**File**: `src\core\rl\LearningObjectives.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ObjectiveStatus`

**Line**: 11  
**Inherits**: Enum  
**Methods**: 0

[TIP] **Suggested split**: Move to `objectivestatus.py`

---

### 2. `ObjectiveType`

**Line**: 18  
**Inherits**: Enum  
**Methods**: 0

[TIP] **Suggested split**: Move to `objectivetype.py`

---

### 3. `LearningObjective`

**Line**: 25  
**Methods**: 3

Represents a learning objective with tracking and evaluation.

[TIP] **Suggested split**: Move to `learningobjective.py`

---

### 4. `ObjectiveConstraint`

**Line**: 83  
**Methods**: 1

Defines a constraint that must be satisfied.

[TIP] **Suggested split**: Move to `objectiveconstraint.py`

---

### 5. `ObjectiveTracker`

**Line**: 97  
**Methods**: 14

Manages high-level goals for the self-improving fleet.

[TIP] **Suggested split**: Move to `objectivetracker.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
