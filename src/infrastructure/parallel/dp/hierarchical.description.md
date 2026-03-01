# hierarchical

**File**: `src\infrastructure\parallel\dp\hierarchical.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 112  
**Complexity**: 6 (moderate)

## Overview

Hierarchical DP coordinator with locality awareness.

## Classes (1)

### `HierarchicalDPCoordinator`

Hierarchical DP coordinator with locality awareness.

**Methods** (6):
- `__init__(self, num_local_coordinators, workers_per_coordinator, locality_groups)`
- `route_request(self, request_id, hint_locality)`
- `complete_request(self, coordinator_idx, worker_id, latency_ms, success)`
- `global_step_sync(self)`
- `global_wave_sync(self)`
- `get_global_metrics(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `src.infrastructure.parallel.dp.engine.DPEngineCoreProc`
- `src.infrastructure.parallel.dp.types.DPConfig`
- `src.infrastructure.parallel.dp.types.DPRole`
- `threading`
- `typing.Any`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
