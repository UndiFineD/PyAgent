# MetaOrchestratorAgent

**File**: `src\classes\orchestration\MetaOrchestratorAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 131  
**Complexity**: 7 (moderate)

## Overview

High-level goal manager and recursive orchestrator.
Manages complex objectives by breaking them down into sub-goals and delegating to specialized agents.

## Classes (1)

### `MetaOrchestratorAgent`

**Inherits from**: BaseAgent

The 'Brain' of the Agent OS. Manages goals, resources, and fleet coordination.

**Methods** (7):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `execute_by_goal(self, goal)`
- `solve_complex_objective(self, objective, depth)`
- `_enrich_args(self, args)`
- `recursive_solve(self, objective, depth)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (11):
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.context.GlobalContextEngine.GlobalContextEngine`
- `src.classes.fleet.FleetManager.FleetManager`
- `src.classes.orchestration.ToolRegistry.ToolRegistry`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
