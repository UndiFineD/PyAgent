# Class Breakdown: enums

**File**: `src\infrastructure\engine\scheduling\priority\enums.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TaskPriority`

**Line**: 25  
**Inherits**: Enum  
**Methods**: 0

Task priority levels.

[TIP] **Suggested split**: Move to `taskpriority.py`

---

### 2. `TaskState`

**Line**: 35  
**Inherits**: Enum  
**Methods**: 0

Task execution state.

[TIP] **Suggested split**: Move to `taskstate.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
