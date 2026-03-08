# automem_core

**File**: `src\core\memory\automem_core.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 44 imports  
**Lines**: 597  
**Complexity**: 26 (complex)

## Overview

PyAgent AutoMem Memory System Integration.

Based on the exceptional AutoMem memory system (90.53% LoCoMo benchmark).
Implements graph-vector hybrid memory with FalkorDB + Qdrant for revolutionary
conversational memory capabilities.

## Classes (5)

### `MemoryConfig`

Configuration for AutoMem memory system.

### `Memory`

Represents a single memory with metadata.

### `AutoMemCore`

AutoMem Memory System Core.

Implements graph-vector hybrid memory with FalkorDB + Qdrant.
Based on the world's highest-performing memory system (90.53% LoCoMo benchmark).

**Methods** (16):
- `__init__(self, config)`
- `_ensure_vector_collection(self)`
- `store_memory(self, content, tags, importance, metadata)`
- `_store_in_graph(self, memory)`
- `_store_in_vector(self, memory)`
- `_generate_embedding(self, content)`
- `recall_memories(self, query, tags, limit, min_score)`
- `_filter_by_tags(self, results, tags)`
- `_matches_tag_filter(self, memory_tags, filter_tags)`
- `_hybrid_score(self, query, query_vector, vector_results)`
- ... and 6 more methods

### `MemoryConsolidator`

Memory consolidation system with neuroscience-inspired cycles.

Implements decay, creative, cluster, and forget consolidation types.

**Methods** (9):
- `__init__(self, memory_core, interval_hours)`
- `start(self)`
- `stop(self)`
- `_consolidation_loop(self)`
- `_run_consolidation_cycle(self)`
- `_decay_memories(self)`
- `_creative_consolidation(self)`
- `_cluster_memories(self)`
- `_forget_memories(self)`

### `PointStruct`

Class PointStruct implementation.

**Methods** (1):
- `__init__(self, id, vector, payload)`

## Dependencies

**Imports** (44):
- `__future__.annotations`
- `collections.Counter`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timedelta`
- `datetime.timezone`
- `falkordb.FalkorDB`
- `hashlib`
- `json`
- `logging`
- `math`
- `openai.OpenAI`
- `os`
- `pathlib.Path`
- ... and 29 more

---
*Auto-generated documentation*
