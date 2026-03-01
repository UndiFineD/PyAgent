# SchemaManager

**File**: `src\classes\fleet\SchemaManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 31  
**Complexity**: 4 (simple)

## Overview

Fleet-wide manager for database schema discovery and metadata storage.

## Classes (1)

### `SchemaManager`

Discovers and caches database schemas across the fleet.

**Methods** (4):
- `__init__(self)`
- `register_schema(self, db_id, tables)`
- `get_context_for_agent(self, db_id)`
- `list_known_databases(self)`

## Dependencies

**Imports** (4):
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
