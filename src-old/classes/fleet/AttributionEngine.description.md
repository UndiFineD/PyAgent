# AttributionEngine

**File**: `src\classes\fleet\AttributionEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 95  
**Complexity**: 7 (moderate)

## Overview

Attribution Engine for PyAgent.
Tracks the lineage and provenance of every generated piece of content or code.

## Classes (1)

### `AttributionEngine`

Records the 'who, when, and how' for all system outputs (Phase 185).

**Methods** (7):
- `__init__(self, workspace_root)`
- `_load(self)`
- `apply_licensing(self, file_path)`
- `record_attribution(self, agent_id, content, task_context)`
- `_save(self)`
- `get_lineage(self, content_hash)`
- `get_summary(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `hashlib`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `src.infrastructure.fleet.core.AttributionCore.AttributionCore`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
