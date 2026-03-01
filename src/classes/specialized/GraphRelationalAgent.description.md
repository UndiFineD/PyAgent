# GraphRelationalAgent

**File**: `src\classes\specialized\GraphRelationalAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 88  
**Complexity**: 8 (moderate)

## Overview

GraphRelationalAgent for PyAgent.
Implements hybrid indexing using vector embeddings and structured knowledge graphs.
Focuses on tracking entity relationships (e.g., Agent -> depends_on -> Tool).

## Classes (1)

### `GraphRelationalAgent`

**Inherits from**: BaseAgent

Hybrid RAG agent combining Graph-based relationships and Vector search.

**Methods** (8):
- `__init__(self, file_path)`
- `_load_graph(self)`
- `_save_graph(self)`
- `add_entity(self, name, entity_type, properties)`
- `add_relation(self, source, relation_type, target)`
- `query_relationships(self, entity_name)`
- `hybrid_search(self, query)`
- `improve_content(self, input_text)`

## Dependencies

**Imports** (10):
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
