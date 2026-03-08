# ScalingCore

**File**: `src\classes\fleet\ScalingCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 32  
**Complexity**: 4 (simple)

## Overview

ScalingCore logic for fleet expansion.
Pure logic for computing moving averages and scaling decisions.

## Classes (1)

### `ScalingCore`

Class ScalingCore implementation.

**Methods** (4):
- `__init__(self, scale_threshold, window_size)`
- `add_metric(self, key, value)`
- `should_scale(self, key)`
- `get_avg_latency(self, key)`

## Dependencies

**Imports** (3):
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
