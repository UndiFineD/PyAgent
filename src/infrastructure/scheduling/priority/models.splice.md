# Class Breakdown: models

**File**: `src\infrastructure\scheduling\priority\models.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TaskStats`

**Line**: 13  
**Methods**: 3

Statistics for task execution.

[TIP] **Suggested split**: Move to `taskstats.py`

---

### 2. `ScheduledTask`

**Line**: 51  
**Inherits**: Unknown  
**Methods**: 1

A task scheduled for execution.

[TIP] **Suggested split**: Move to `scheduledtask.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
