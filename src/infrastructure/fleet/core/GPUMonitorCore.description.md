# GPUMonitorCore

**File**: `src\infrastructure\fleet\core\GPUMonitorCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 4 imports  
**Lines**: 77  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for GPUMonitorCore.

## Classes (2)

### `GPUMetrics`

Pure data class for GPU telemetry.

**Methods** (1):
- `vram_percent(self)`

### `GPUMonitorCore`

Pure logic for GPU health and pressure calculation.
Complies with Core/Shell pattern (Side-effect free).

**Methods** (3):
- `calculate_vram_pressure(metrics)`
- `identify_optimal_gpu(metrics)`
- `needs_throttling(metrics, temp_threshold, vram_threshold_percent)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `dataclasses.dataclass`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
