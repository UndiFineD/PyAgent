# WeightOrchestrator

**File**: `src\classes\orchestration\WeightOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 79  
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
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
