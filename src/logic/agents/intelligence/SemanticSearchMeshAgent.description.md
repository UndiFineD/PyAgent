# SemanticSearchMeshAgent

**File**: `src\logic\agents\intelligence\SemanticSearchMeshAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 149  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for SemanticSearchMeshAgent.

## Classes (1)

### `SemanticSearchMeshAgent`

Coordinates federated semantic search across multiple providers and fleet shards.
Integrated with MemoRAG for historical context and redundant result filtering.

**Methods** (4):
- `__init__(self, workspace_path)`
- `register_shard(self, shard_id, metadata)`
- `federated_search(self, query_embedding, limit)`
- `replicate_shard(self, source_shard, target_node)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `asyncio`
- `rust_core`
- `src.core.base.Version.VERSION`
- `src.logic.agents.intelligence.MemoRAGAgent.MemoRAGAgent`
- `src.logic.agents.intelligence.core.SearchMeshCore.SearchMeshCore`
- `typing.Any`

---
*Auto-generated documentation*
