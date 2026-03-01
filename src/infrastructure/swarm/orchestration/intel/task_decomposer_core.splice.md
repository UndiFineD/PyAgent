# Class Breakdown: task_decomposer_core

**File**: `src\infrastructure\swarm\orchestration\intel\task_decomposer_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PlanStep`

**Line**: 35  
**Methods**: 0

Represents a single step in a decomposed task plan.

[TIP] **Suggested split**: Move to `planstep.py`

---

### 2. `TaskDecomposerCore`

**Line**: 44  
**Methods**: 3

Pure logic for task decomposition.
Handles heuristic-based planning and plan summarization.

[TIP] **Suggested split**: Move to `taskdecomposercore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
