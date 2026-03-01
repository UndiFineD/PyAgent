# Class Breakdown: file_lock_manager

**File**: `src\core\base\common\utils\file_lock_manager.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LockProxy`

**Line**: 25  
**Methods**: 1

A proxy object for a held lock.

[TIP] **Suggested split**: Move to `lockproxy.py`

---

### 2. `FileLockManager`

**Line**: 33  
**Methods**: 6

Manager for coordinating file-system level locks.
Delegates to LockCore for the underlying synchronization logic.

[TIP] **Suggested split**: Move to `filelockmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
