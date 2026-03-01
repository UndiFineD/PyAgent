# MemoryPruningAgent

**File**: `src\classes\specialized\MemoryPruningAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 78  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for MemoryPruningAgent.

## Classes (1)

### `MemoryPruningAgent`

Optimizes Long-Term Memory (LTM) by ranking importance and 
pruning low-utility or stale data slices.

**Methods** (4):
- `__init__(self, workspace_path)`
- `rank_memory_importance(self, memory_entry)`
- `select_pruning_targets(self, memory_list, threshold)`
- `generate_archival_plan(self, memory_list)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
