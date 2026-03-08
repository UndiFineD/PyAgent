# EvolutionEngine

**File**: `src\classes\fleet\EvolutionEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 51  
**Complexity**: 4 (simple)

## Overview

Engine for autonomous agent creation.
Allows agents to generate new, specialized agent files to expand fleet capabilities.

## Classes (1)

### `EvolutionEngine`

Manages the autonomous generation of new agent types.
Shell for EvolutionCore.

**Methods** (4):
- `__init__(self, workspace_root)`
- `generate_agent(self, name, capabilities, base_type)`
- `optimize_hyperparameters(self, fleet_stats)`
- `register_generated_agent(self, fleet_manager, name, path)`

## Dependencies

**Imports** (7):
- `EvolutionCore.EvolutionCore`
- `logging`
- `os`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
