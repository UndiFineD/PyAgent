# FractalOrchestrator

**File**: `src\infrastructure\orchestration\swarm\FractalOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 82  
**Complexity**: 3 (simple)

## Overview

FractalOrchestrator: Manages self-similar sub-swarm structures.
Handles recursive task delegation to specialized fleet clusters.

## Classes (1)

### `FractalOrchestrator`

Orchestrator for managing fractal (self-similar) swarm hierarchies.
Facilitates the creation and coordination of sub-swarms for complex tasks.

**Methods** (3):
- `__init__(self, fleet)`
- `create_sub_swarm(self, parent_task_id, required_capabilities)`
- `delegate_to_sub_swarm(self, swarm_id, sub_task)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `src.core.base.Version.VERSION`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
