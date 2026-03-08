# database_access_core

**File**: `src\core\base\logic\processing\database_access_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 154  
**Complexity**: 6 (moderate)

## Overview

Module: database_access_core
Core logic for ODBC database operations.
Implements database connection and query patterns from ADSyncDump-BOF.

## Classes (1)

### `DatabaseAccessCore`

Core class for ODBC database operations.

**Methods** (6):
- `__init__(self)`
- `connect(self, connection_string)`
- `execute_query(self, query)`
- `disconnect(self)`
- `get_last_error(self)`
- `_get_error_message(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `ctypes`
- `ctypes.wintypes`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
