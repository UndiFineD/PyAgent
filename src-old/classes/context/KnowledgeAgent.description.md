# KnowledgeAgent

**File**: `src\classes\context\KnowledgeAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 19 imports  
**Lines**: 485  
**Complexity**: 15 (moderate)

## Overview

Agent specializing in Workspace Knowledge and Codebase Context (RAG-lite).

## Classes (1)

### `KnowledgeAgent`

**Inherits from**: BaseAgent

Agent that scans the workspace to provide deep context using MIRIX 6-tier memory.

**Methods** (15):
- `__init__(self, file_path, fleet)`
- `_init_chroma(self)`
- `build_index(self)`
- `record_tier_memory(self, tier, content, metadata)`
- `query_mirix(self, tier, query, limit)`
- `build_vector_index(self)`
- `semantic_search(self, query, n_results)`
- `scan_workspace(self, query)`
- `find_backlinks(self, file_name)`
- `auto_update_backlinks(self, directory)`
- ... and 5 more methods

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `chromadb`
- `datetime.datetime`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.engines.ContextCompressor.ContextCompressor`
- `src.logic.agents.cognitive.context.engines.GraphContextEngine.GraphContextEngine`
- `src.logic.agents.cognitive.context.engines.KnowledgeCore.KnowledgeCore`
- `src.logic.agents.cognitive.context.engines.MemoryEngine.MemoryEngine`
- ... and 4 more

---
*Auto-generated documentation*
