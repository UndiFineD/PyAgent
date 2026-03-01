# Class Breakdown: enums

**File**: `src\infrastructure\engine\request_queue\enums.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SchedulingPolicy`

**Line**: 25  
**Inherits**: Enum  
**Methods**: 0

Request scheduling policy.

[TIP] **Suggested split**: Move to `schedulingpolicy.py`

---

### 2. `RequestStatus`

**Line**: 35  
**Inherits**: Enum  
**Methods**: 0

Status of a request in the queue.

[TIP] **Suggested split**: Move to `requeststatus.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
