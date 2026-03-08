# SQLAgent

**File**: `src\classes\specialized\SQLAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 102  
**Complexity**: 7 (moderate)

## Overview

Agent specializing in SQL database interaction and query optimization.

## Classes (1)

### `SQLQueryAgent`

**Inherits from**: BaseAgent

Enables the fleet to interact with relational databases and unified data sources (MindsDB style).

**Methods** (7):
- `__init__(self, file_path)`
- `unify_sources(self, source_identities)`
- `connect_mcp_datasource(self, mcp_server_url)`
- `connect_local(self, db_path)`
- `execute_query(self, query)`
- `get_table_schema(self, table_name)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `sqlite3`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
