# StatusManager

**File**: `src\classes\orchestration\StatusManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 75  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for StatusManager.

## Classes (1)

### `StatusManager`

Manages project execution status for the DirectorAgent and GUI.

**Methods** (8):
- `__init__(self)`
- `clear_status(self)`
- `start_project(self, goal, steps_count)`
- `add_step(self, agent, file, prompt)`
- `update_step_status(self, index, status, result)`
- `finish_project(self, success)`
- `_read(self)`
- `_write(self, data)`

## Dependencies

**Imports** (7):
- `datetime.datetime`
- `json`
- `os`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
