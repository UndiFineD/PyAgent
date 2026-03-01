# SystemHealthMonitor

**File**: `src\infrastructure\backend\SystemHealthMonitor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 185  
**Complexity**: 9 (moderate)

## Overview

Auto-extracted class from agent_backend.py

## Classes (1)

### `SystemHealthMonitor`

Monitors backend health and manages failover.
Integrated with StabilityCore for advanced fleet-wide stasis detection.

**Methods** (9):
- `__init__(self, health_threshold, window_size)`
- `record_success(self, backend, latency_ms)`
- `record_failure(self, backend, latency_ms)`
- `_update_status(self, backend)`
- `is_healthy(self, backend)`
- `get_status(self, backend)`
- `get_all_status(self)`
- `get_healthiest(self, backends)`
- `calculate_global_stability(self, anomalies)`

## Dependencies

**Imports** (12):
- `SystemHealthStatus.SystemHealthStatus`
- `SystemState.SystemState`
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `src.observability.stats.analysis.FleetMetrics`
- `src.observability.stats.core.StabilityCore.StabilityCore`
- `threading`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
