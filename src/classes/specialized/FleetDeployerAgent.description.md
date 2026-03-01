# FleetDeployerAgent

**File**: `src\classes\specialized\FleetDeployerAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 133  
**Complexity**: 1 (simple)

## Overview

FleetDeployerAgent for PyAgent.
Specializes in autonomous containerization, Dockerfile generation, 
and managing node spawning across environments.

## Classes (1)

### `FleetDeployerAgent`

**Inherits from**: BaseAgent

Manages the lifecycle of fleet nodes, including containerization and deployment.

**Methods** (1):
- `__init__(self, file_path)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `asyncio`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
