# database_access_mixin

**File**: `src\core\base\mixins\database_access_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 52  
**Complexity**: 5 (moderate)

## Overview

Module: database_access_mixin
Database access mixin for BaseAgent, implementing ODBC database operations.
Inspired by ADSyncDump-BOF database connection patterns.

## Classes (1)

### `DatabaseAccessMixin`

Mixin providing database access features using ODBC.

**Methods** (5):
- `__init__(self)`
- `connect_odbc(self, connection_string)`
- `execute_query(self, query)`
- `disconnect(self)`
- `get_last_error(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `platform`
- `src.core.base.logic.processing.database_access_core.DatabaseAccessCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
