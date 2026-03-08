# ModelForgeAgent

**File**: `src\classes\specialized\ModelForgeAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 15 imports  
**Lines**: 130  
**Complexity**: 1 (simple)

## Overview

Model Forge Agent for PyAgent.
Specializes in local fine-tuning and model optimization (LoRA/QLoRA).

## Classes (1)

### `ModelForgeAgent`

**Inherits from**: BaseAgent

Orchestrates local model fine-tuning and adapter management.

**Methods** (1):
- `__init__(self, path)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `asyncio`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `src.logic.agents.system.core.ModelRegistryCore.ModelRegistryCore`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
