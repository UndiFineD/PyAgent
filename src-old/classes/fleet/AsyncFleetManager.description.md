# AsyncFleetManager

**File**: `src\classes\fleet\AsyncFleetManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 88  
**Complexity**: 3 (simple)

## Overview

An enhanced FleetManager that supports parallel execution of agent workflows.

## Classes (1)

### `AsyncFleetManager`

**Inherits from**: FleetManager

Executes agent workflows in parallel using a thread pool.

**Methods** (3):
- `__init__(self, workspace_root, max_workers)`
- `execute_workflow_async(self, task, workflow_steps)`
- `_run_single_step(self, step, workflow_id)`

## Dependencies

**Imports** (12):
- `concurrent.futures`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.coder.SecurityGuardAgent.SecurityGuardAgent`
- `src.classes.context.KnowledgeAgent.KnowledgeAgent`
- `src.classes.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Type`

---
*Auto-generated documentation*
