# Class Breakdown: scheduler_output

**File**: `src\infrastructure\engine\scheduling\v2\scheduler_output.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ScheduledSequence`

**Line**: 26  
**Methods**: 0

Represents a sequence scheduled for execution.

[TIP] **Suggested split**: Move to `scheduledsequence.py`

---

### 2. `SchedulerOutput`

**Line**: 39  
**Methods**: 3

Comprehensive output structure containing all info for the execution engine.
Part of Phase 54 Async Evolution.

[TIP] **Suggested split**: Move to `scheduleroutput.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
