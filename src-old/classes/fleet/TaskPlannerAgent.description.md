# TaskPlannerAgent

**File**: `src\classes\fleet\TaskPlannerAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 118  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in breaking down complex tasks into executable workflows.

## Classes (1)

### `TaskPlannerAgent`

**Inherits from**: BaseAgent

Orchestrator that plans multi-agent workflows.

**Methods** (5):
- `__init__(self, file_path)`
- `generate_shared_dependencies(self, prompt)`
- `_get_default_content(self)`
- `create_plan(self, user_request)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `json`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
