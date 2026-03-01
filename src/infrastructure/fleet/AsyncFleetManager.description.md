# AsyncFleetManager

**File**: `src\infrastructure\fleet\AsyncFleetManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 254  
**Complexity**: 1 (simple)

## Overview

An enhanced FleetManager that supports parallel execution of agent workflows.

## Classes (1)

### `AsyncFleetManager`

**Inherits from**: FleetManager

Executes agent workflows in parallel using native asyncio.
Supports dependency-aware batching for optimized execution (Phase 232).

**Methods** (1):
- `__init__(self, workspace_root, max_workers)`

## Dependencies

**Imports** (17):
- `FleetManager.FleetManager`
- `WorkflowState.WorkflowState`
- `__future__.annotations`
- `asyncio`
- `inspect`
- `logging`
- `src.core.base.DependencyGraph.DependencyGraph`
- `src.core.base.version.VERSION`
- `src.infrastructure.orchestration.LockManager.LockManager`
- `src.logic.agents.cognitive.KnowledgeAgent.KnowledgeAgent`
- `src.logic.agents.security.SecurityGuardAgent.SecurityGuardAgent`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 2 more

---
*Auto-generated documentation*
