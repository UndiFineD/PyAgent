# LongTermMemory

**File**: `src\core\base\common\utils\LongTermMemory.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 112  
**Complexity**: 5 (moderate)

## Overview

Long-term memory for agents using vector storage.

## Classes (1)

### `LongTermMemory`

Manages persistent conversational and factual memory for agents.

**Methods** (5):
- `__init__(self, collection_name, persist_directory)`
- `_init_db(self)`
- `store(self, content, metadata, tags)`
- `query(self, query_text, n_results, filter_tags)`
- `clear(self)`

## Dependencies

**Imports** (10):
- `chromadb`
- `chromadb.config.Settings`
- `datetime.datetime`
- `json`
- `logging`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
