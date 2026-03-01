# FleetRoutingCore

**File**: `src\infrastructure\fleet\FleetRoutingCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 200  
**Complexity**: 4 (simple)

## Overview

Routing logic for the FleetManager.

## Classes (1)

### `FleetRoutingCore`

Handles task routing and capability-based agent selection.

**Methods** (4):
- `__init__(self, fleet)`
- `_ensure_agents_loaded(self, goal)`
- `_select_optimized_tool(self, goal, candidates)`
- `route_task(self, task_type, task_data)`

## Dependencies

**Imports** (8):
- `FleetManager.FleetManager`
- `__future__.annotations`
- `asyncio`
- `inspect`
- `logging`
- `time`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
