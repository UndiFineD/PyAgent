# ResourceMonitor

**File**: `src\classes\stats\ResourceMonitor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 80  
**Complexity**: 4 (simple)

## Overview

Engine for monitoring system resources (CPU, Memory, Disk).

## Classes (1)

### `ResourceMonitor`

Monitors local system load to inform agent execution strategies.

**Methods** (4):
- `__init__(self, workspace_root)`
- `get_current_stats(self)`
- `save_stats(self)`
- `get_execution_recommendation(self)`

## Dependencies

**Imports** (9):
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `platform`
- `psutil`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
