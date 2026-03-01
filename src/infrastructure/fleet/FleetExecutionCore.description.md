# FleetExecutionCore

**File**: `src\infrastructure\fleet\FleetExecutionCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 15 imports  
**Lines**: 286  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for FleetExecutionCore.

## Classes (1)

### `FleetExecutionCore`

Handles core workflow execution and task reliability logic for the Fleet.

**Methods** (2):
- `__init__(self, fleet)`
- `_check_ethics(self, task)`

## Dependencies

**Imports** (15):
- `FleetManager.FleetManager`
- `__future__.annotations`
- `asyncio`
- `inspect`
- `logging`
- `src.core.base.Version.VERSION`
- `src.core.base.models.AgentPriority`
- `src.infrastructure.fleet.WorkflowState.WorkflowState`
- `time`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
