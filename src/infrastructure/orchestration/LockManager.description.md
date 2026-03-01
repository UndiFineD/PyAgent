# LockManager

**File**: `src\infrastructure\orchestration\LockManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 143  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for LockManager.

## Classes (1)

### `LockManager`

Phase 242/152: Distributed & Async-Ready Lock Manager.
Supports memory-based (threading.Lock/asyncio.Lock) and file-based (portalocker) locking.

**Methods** (8):
- `__new__(cls)`
- `__init__(self, lock_dir)`
- `get_memory_lock(self, resource_id)`
- `get_async_memory_lock(self, resource_id)`
- `_sync_file_lock_acquire(self, resource_path, timeout)`
- `_sync_file_lock_release(self, resource_path)`
- `file_lock(self, resource_path, timeout)`
- `acquire(self, resource_id, lock_type, timeout)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `asyncio`
- `contextlib.asynccontextmanager`
- `contextlib.contextmanager`
- `logging`
- `os`
- `pathlib.Path`
- `portalocker`
- `threading`
- `typing.Any`
- `typing.ContextManager`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
