# GlobalContextCore

**File**: `src\classes\context\GlobalContextCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 85  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for GlobalContextCore.

## Classes (1)

### `GlobalContextCore`

Pure logic for GlobalContext.
Handles data merging, pruning, and summary formatting.
No I/O or direct disk access.

**Methods** (6):
- `partition_memory(self, memory, max_entries_per_shard)`
- `prepare_fact(self, key, value)`
- `prepare_insight(self, insight, source_agent)`
- `merge_entity_info(self, existing, new_attributes)`
- `prune_lessons(self, lessons, max_lessons)`
- `generate_markdown_summary(self, memory)`

## Dependencies

**Imports** (6):
- `datetime.datetime`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `zlib`

---
*Auto-generated documentation*
