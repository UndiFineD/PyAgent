# SqlAgent

**File**: `src\infrastructure\compute\backend\SqlAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 231  
**Complexity**: 10 (moderate)

## Overview

Python module containing implementation for SqlAgent.

## Classes (1)

### `SqlAgent`

Relational metadata overlay for compressed interaction shards.

**Methods** (10):
- `__init__(self, db_path, shards_dir)`
- `_init_db(self)`
- `optimize_db(self)`
- `_rotate_metadata_shard(self)`
- `record_lesson(self, interaction_id, text, category)`
- `get_intelligence_summary(self)`
- `index_shards(self)`
- `query_interactions(self, sql_where)`
- `record_debt(self, file_path, issue_type, message, fixed)`
- `bulk_record_interactions(self, interaction_data)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `gzip`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `sqlite3`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
