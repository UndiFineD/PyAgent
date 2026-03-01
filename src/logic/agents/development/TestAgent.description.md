# TestAgent

**File**: `src\logic\agents\development\TestAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 77  
**Complexity**: 4 (simple)

## Overview

Agent specializing in automated testing and coverage analysis.
Inspired by SGI-Bench and py.test.

## Classes (1)

### `TestAgent`

**Inherits from**: BaseAgent

Executes unit and integration tests and analyzes failures.

**Methods** (4):
- `__init__(self, file_path)`
- `run_tests(self, path)`
- `run_file_tests(self, file_path)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
