# session_lock_core

**File**: `src\core\base\logic\core\session_lock_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 54  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for session_lock_core.

## Classes (1)

### `SessionLockCore`

Core for managing multi-tenant session locking and space isolation.

**Methods** (2):
- `__init__(self, storage_path)`
- `validate_space(self, tenant_id, space_id)`

## Dependencies

**Imports** (6):
- `datetime.datetime`
- `os`
- `secrets`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
