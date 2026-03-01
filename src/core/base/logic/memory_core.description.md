# memory_core

**File**: `src\core\base\logic\memory_core.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 19 imports  
**Lines**: 555  
**Complexity**: 7 (moderate)

## Overview

Memory Core - Hybrid graph-vector memory system
Based on AutoMem patterns: FalkorDB + Qdrant hybrid architecture

## Classes (6)

### `MemoryNode`

Represents a memory node in the graph

**Methods** (1):
- `__post_init__(self)`

### `MemoryRelation`

Represents a relationship between memory nodes

**Methods** (1):
- `__post_init__(self)`

### `MemoryStore`

**Inherits from**: ABC

Abstract base class for memory storage backends

### `GraphMemoryStore`

**Inherits from**: MemoryStore

Graph-based memory store using relationship patterns
Based on AutoMem's FalkorDB patterns

**Methods** (1):
- `__init__(self)`

### `VectorMemoryStore`

**Inherits from**: MemoryStore

Vector-based memory store for semantic similarity
Based on AutoMem's Qdrant patterns

**Methods** (2):
- `__init__(self)`
- `_cosine_similarity(self, a, b)`

### `HybridMemoryCore`

Hybrid graph-vector memory system
Based on AutoMem's dual storage architecture

**Methods** (2):
- `__init__(self, graph_store, vector_store)`
- `_cosine_similarity(self, a, b)`

## Dependencies

**Imports** (19):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timezone`
- `json`
- `logging`
- `math`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 4 more

---
*Auto-generated documentation*
