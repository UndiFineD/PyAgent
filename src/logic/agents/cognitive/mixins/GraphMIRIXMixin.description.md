# GraphMIRIXMixin

**File**: `src\logic\agents\cognitive\mixins\GraphMIRIXMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 111  
**Complexity**: 3 (simple)

## Overview

MIRIX memory logic for GraphMemoryAgent.

## Classes (1)

### `GraphMIRIXMixin`

Mixin for MIRIX 6-component memory logic.

**Methods** (3):
- `store_mirix_memory(self, category, name, data)`
- `decay_memories(self, threshold_score)`
- `record_outcome(self, entity_id, success)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseUtilities.as_tool`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
