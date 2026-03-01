# Class Breakdown: models

**File**: `src\infrastructure\engine\request_queue\models.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RequestPriority`

**Line**: 30  
**Methods**: 2

Composite priority for request scheduling.

Lower values = higher priority (processed first).

[TIP] **Suggested split**: Move to `requestpriority.py`

---

### 2. `QueuedRequest`

**Line**: 56  
**Methods**: 5

Request wrapper for queue management.

Contains request data and queue metadata.

[TIP] **Suggested split**: Move to `queuedrequest.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
