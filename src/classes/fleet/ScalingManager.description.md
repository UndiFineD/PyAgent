# ScalingManager

**File**: `src\classes\fleet\ScalingManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 42  
**Complexity**: 4 (simple)

## Overview

Manager for dynamic scaling of the agent fleet.
Monitors system load and spawns new agent instances as needed.

## Classes (1)

### `ScalingManager`

Shell for ScalingManager.
Handles fleet orchestration while delegating logic to ScalingCore.

**Methods** (4):
- `__init__(self, fleet_manager)`
- `record_metric(self, agent_name, latency)`
- `_execute_scale_out(self, agent_name)`
- `get_scaling_status(self)`

## Dependencies

**Imports** (8):
- `ScalingCore.ScalingCore`
- `logging`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Type`

---
*Auto-generated documentation*
