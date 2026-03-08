# GraphBeadsMixin

**File**: `src\logic\agents\cognitive\mixins\GraphBeadsMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 92  
**Complexity**: 3 (simple)

## Overview

Beads task logic for GraphMemoryAgent.

## Classes (1)

### `GraphBeadsMixin`

Mixin for Beads task graph logic.

**Methods** (3):
- `create_task(self, title, parent_id, priority)`
- `add_dependency(self, blocker_id, blocked_id)`
- `compact_memory(self, threshold_days)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseUtilities.as_tool`

---
*Auto-generated documentation*
