# MemoryEngine

**File**: `src\classes\context\MemoryEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 40  
**Complexity**: 1 (simple)

## Overview

Engine for persistent episodic memory of agent actions and outcomes.

## Classes (1)

### `MemoryEngine`

**Inherits from**: MemoryStorageMixin, MemoryEpisodeMixin, MemorySearchMixin

Stores and retrieves historical agent contexts and lessons learned.

**Methods** (1):
- `__init__(self, workspace_root)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `memory_mixins.MemoryEpisodeMixin.MemoryEpisodeMixin`
- `memory_mixins.MemorySearchMixin.MemorySearchMixin`
- `memory_mixins.MemoryStorageMixin.MemoryStorageMixin`
- `pathlib.Path`
- `src.core.base.Version.VERSION`
- `src.logic.agents.cognitive.context.engines.MemoryCore.MemoryCore`
- `typing.Any`

---
*Auto-generated documentation*
