# WeightOrchestrator

**File**: `src\infrastructure\orchestration\WeightOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 95  
**Complexity**: 8 (moderate)

## Overview

WeightOrchestrator for PyAgent.
Manages the lifecycle of neural weights (LoRA/QLoRA adapters) across the fleet.
Coordinates between the ModelForgeAgent and individual agents to hot-swap capabilities.

## Classes (1)

### `WeightOrchestrator`

**Inherits from**: BaseAgent

Orchestrates the distribution and activation of model weights across the fleet.

**Methods** (8):
- `__init__(self, file_path)`
- `_load_registry(self)`
- `_save_registry(self)`
- `activate_adapter(self, agent_name, adapter_name)`
- `get_active_adapter(self, agent_name)`
- `deactivate_adapter(self, agent_name)`
- `list_registrations(self)`
- `improve_content(self, input_text)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
