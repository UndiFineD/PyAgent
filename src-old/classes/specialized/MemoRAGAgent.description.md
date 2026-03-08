# MemoRAGAgent

**File**: `src\classes\specialized\MemoRAGAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 105  
**Complexity**: 5 (moderate)

## Overview

Agent implementing MemoRAG patterns for global context understanding.
Generates 'clues' from global memory to improve retrieval accuracy.
Ref: https://github.com/qhjqhj00/MemoRAG

## Classes (1)

### `MemoRAGAgent`

**Inherits from**: BaseAgent

Memory-Augmented RAG agent for deep context discovery with sharding.

**Methods** (5):
- `__init__(self, file_path)`
- `memorise_to_shard(self, context, shard_name)`
- `recall_clues_from_shard(self, query, shard_name)`
- `list_shards(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `rust_core`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `src.logic.agents.intelligence.core.SynthesisCore.SynthesisCore`

---
*Auto-generated documentation*
