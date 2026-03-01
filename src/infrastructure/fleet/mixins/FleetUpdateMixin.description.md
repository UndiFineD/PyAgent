# FleetUpdateMixin

**File**: `src\infrastructure\fleet\mixins\FleetUpdateMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 84  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for FleetUpdateMixin.

## Classes (1)

### `FleetUpdateMixin`

Mixin for FleetManager to support autonomous periodic updates.
Checks for repository updates every 15 minutes.

**Methods** (3):
- `init_update_service(self, interval_seconds)`
- `_update_loop(self)`
- `_run_git_pull(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `os`
- `pathlib.Path`
- `src.observability.StructuredLogger.StructuredLogger`
- `subprocess`
- `threading`
- `time`

---
*Auto-generated documentation*
