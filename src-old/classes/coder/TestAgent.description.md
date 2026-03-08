# TestAgent

**File**: `src\classes\coder\TestAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 64  
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

**Imports** (11):
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `subprocess`
- `sys`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
