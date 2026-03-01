# ConnectionPool

**File**: `src\classes\backend\ConnectionPool.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 167  
**Complexity**: 10 (moderate)

## Overview

Auto-extracted class from agent_backend.py

## Classes (1)

### `ConnectionPool`

Manages a pool of reusable connections with Phase 108 status caching.
Reduces connection overhead and prevents repeated failure pings by
caching 'working' status for 15 minutes.

**Methods** (10):
- `__init__(self, max_connections, timeout_s, cache_file)`
- `_load_status_cache(self)`
- `_save_status_cache(self)`
- `is_backend_working(self, backend)`
- `set_backend_status(self, backend, working)`
- `acquire(self, backend)`
- `release(self, backend, connection)`
- `_create_connection(self, backend)`
- `get_stats(self)`
- `close_all(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `threading`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
