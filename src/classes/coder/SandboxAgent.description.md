# SandboxAgent

**File**: `src\classes\coder\SandboxAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 62  
**Complexity**: 4 (simple)

## Overview

Agent specializing in secure code execution and sandboxed prototyping.
Prevents side effects on the host system by using containerized or WASM environments.

## Classes (1)

### `SandboxAgent`

**Inherits from**: BaseAgent

Executes untrusted code in a controlled environment.

**Methods** (4):
- `__init__(self, file_path)`
- `run_python_sandboxed(self, code)`
- `dry_run_prediction(self, code)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (10):
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.base_agent.utilities.create_main_function`
- `subprocess`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
