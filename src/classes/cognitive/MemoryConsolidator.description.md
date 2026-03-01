# MemoryConsolidator

**File**: `src\classes\cognitive\MemoryConsolidator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 93  
**Complexity**: 6 (moderate)

## Overview

Shell for MemoryConsolidator, handling storage and orchestration.

## Classes (1)

### `MemoryConsolidator`

Manages the 'Sleep & Consolidate' phase for agents.

Acts as the I/O Shell for MemoryConsolidatorCore.

**Methods** (6):
- `__init__(self, storage_path)`
- `record_interaction(self, agent, task, outcome)`
- `sleep_and_consolidate(self)`
- `_load_memory(self)`
- `_save_memory(self, memory)`
- `query_long_term_memory(self, query)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `src.logic.cognitive.MemoryConsolidatorCore.MemoryConsolidatorCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
