# LocalRAGCore

**File**: `src\logic\agents\cognitive\core\LocalRAGCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 3 imports  
**Lines**: 45  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for LocalRAGCore.

## Classes (2)

### `RAGShard`

Metadata for a localized vector shard.

### `LocalRAGCore`

Pure logic for hyper-localized RAG and vector sharding.
Handles shard selection, path-based routing, and context relevance.

**Methods** (3):
- `route_query_to_shards(self, query, query_path, available_shards)`
- `calculate_rerank_score(self, original_score, path_proximity)`
- `extract_local_context_markers(self, content)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `dataclasses.dataclass`
- `typing.List`

---
*Auto-generated documentation*
