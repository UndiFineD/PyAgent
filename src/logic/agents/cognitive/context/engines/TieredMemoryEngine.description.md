# TieredMemoryEngine

**File**: `src\logic\agents\cognitive\context\engines\TieredMemoryEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 30  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for TieredMemoryEngine.

## Classes (1)

### `TieredMemoryEngine`

Manages the 6 memory tiers: Core, Episodic, Semantic, Procedural, Resource, and Knowledge.

**Methods** (5):
- `__init__(self, db_path)`
- `record_memory(self, tier, content, metadata)`
- `query_tier(self, tier, query, limit)`
- `upsert_documents(self, documents, metadatas, ids)`
- `search_workspace(self, query, n_results)`

## Dependencies

**Imports** (5):
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
