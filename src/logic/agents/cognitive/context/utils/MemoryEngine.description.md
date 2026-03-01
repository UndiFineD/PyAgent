# MemoryEngine

**File**: `src\logic\agents\cognitive\context\utils\MemoryEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 176  
**Complexity**: 9 (moderate)

## Overview

Engine for persistent episodic memory of agent actions and outcomes.

## Classes (1)

### `MemoryEngine`

Stores and retrieves historical agent contexts and lessons learned.

**Methods** (9):
- `__init__(self, workspace_root)`
- `_init_db(self)`
- `record_episode(self, agent_name, task, outcome, success, metadata)`
- `update_utility(self, memory_id, increment)`
- `get_lessons_learned(self, query, limit, min_utility)`
- `search_memories(self, query, limit)`
- `save(self)`
- `load(self)`
- `clear(self)`

## Dependencies

**Imports** (10):
- `MemoryCore.MemoryCore`
- `chromadb`
- `datetime.datetime`
- `json`
- `logging`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
