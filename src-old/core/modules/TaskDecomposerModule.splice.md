# Class Breakdown: TaskDecomposerModule

**File**: `src\core\modules\TaskDecomposerModule.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PlanStep`

**Line**: 20  
**Methods**: 0

[TIP] **Suggested split**: Move to `planstep.py`

---

### 2. `TaskDecomposerModule`

**Line**: 26  
**Inherits**: BaseModule  
**Methods**: 5

Consolidated core module for task decomposition.
Migrated from TaskDecomposerCore.

[TIP] **Suggested split**: Move to `taskdecomposermodule.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
