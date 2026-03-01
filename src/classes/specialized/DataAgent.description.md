# DataAgent

**File**: `src\classes\specialized\DataAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 116  
**Complexity**: 6 (moderate)

## Overview

Agent specializing in advanced SQL operations, data analysis, and database management.
Provides execution capabilities and schema discovery.

## Classes (1)

### `DataAgent`

**Inherits from**: BaseAgent

Advanced agent for database interaction and data processing.

**Methods** (6):
- `__init__(self, file_path)`
- `connect(self, db_path)`
- `execute_sql(self, sql)`
- `get_schema(self)`
- `query_to_csv(self, sql, output_path)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `pandas`
- `sqlite3`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
