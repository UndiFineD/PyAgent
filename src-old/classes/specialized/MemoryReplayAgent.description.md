# MemoryReplayAgent

**File**: `src\classes\specialized\MemoryReplayAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 87  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for MemoryReplayAgent.

## Classes (1)

### `MemoryReplayAgent`

Simulates "sleep cycles" for agents where they replay episodic memories
to consolidate knowledge, identify patterns, and prune low-utility data.

**Methods** (4):
- `__init__(self, workspace_path)`
- `start_sleep_cycle(self, episodic_memories)`
- `_evaluate_utility(self, memory)`
- `get_dream_log(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `pathlib.Path`
- `random`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
