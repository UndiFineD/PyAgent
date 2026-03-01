# GPUScalingManager

**File**: `src\classes\fleet\GPUScalingManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 41  
**Complexity**: 3 (simple)

## Overview

GPU scaling manager for specialized agents.
Scales agent pools based on GPU memory pressure and latency.

## Classes (1)

### `GPUScalingManager`

Monitors GPU resources and triggers scaling events.

**Methods** (3):
- `__init__(self, threshold_pct)`
- `monitor_memory_pressure(self)`
- `get_resource_summary(self)`

## Dependencies

**Imports** (4):
- `logging`
- `random`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
