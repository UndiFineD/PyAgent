# Class Breakdown: config

**File**: `src\infrastructure\engine\scheduling\advanced\config.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RequestPriority`

**Line**: 23  
**Inherits**: Enum  
**Methods**: 0

Priority levels for inference requests.

[TIP] **Suggested split**: Move to `requestpriority.py`

---

### 2. `RequestState`

**Line**: 33  
**Inherits**: Enum  
**Methods**: 0

State of an inference request.

[TIP] **Suggested split**: Move to `requeststate.py`

---

### 3. `PreemptionReason`

**Line**: 45  
**Inherits**: Enum  
**Methods**: 0

Reason for request preemption.

[TIP] **Suggested split**: Move to `preemptionreason.py`

---

### 4. `SchedulerConfig`

**Line**: 56  
**Methods**: 0

Configuration for the request scheduler.

[TIP] **Suggested split**: Move to `schedulerconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
