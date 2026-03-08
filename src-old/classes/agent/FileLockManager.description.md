# FileLockManager

**File**: `src\classes\agent\FileLockManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 133  
**Complexity**: 4 (simple)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `FileLockManager`

Manages file locks to prevent concurrent modifications.

Provides advisory file locking to coordinate access between
multiple agent instances or processes.

Attributes:
    locks: Dict of active file locks.
    lock_timeout: Default lock timeout in seconds.

**Methods** (4):
- `__init__(self, lock_timeout)`
- `acquire_lock(self, file_path, lock_type, timeout)`
- `release_lock(self, file_path)`
- `_cleanup_expired_locks(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.models.LockType`
- `src.core.base.utils.FileLock.FileLock`
- `src.core.base.version.VERSION`
- `threading`
- `time`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
