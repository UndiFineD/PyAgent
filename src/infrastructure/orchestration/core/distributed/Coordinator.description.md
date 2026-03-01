# Coordinator

**File**: `src\infrastructure\orchestration\core\distributed\Coordinator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 151  
**Complexity**: 9 (moderate)

## Overview

Data-parallel coordination logic.

## Classes (1)

### `DPCoordinator`

Coordinator for data-parallel engine instances.

Inspired by vLLM's DPCoordinator and dp_lb_pool patterns.
Manages multiple engine instances and distributes requests.

**Methods** (9):
- `__init__(self, parallel_config, load_balancing)`
- `register_engine(self, identity)`
- `deregister_engine(self, engine_id)`
- `select_engine(self, request_id)`
- `update_metrics(self, engine_id, metrics)`
- `set_engine_state(self, engine_id, state)`
- `get_engine_states(self)`
- `num_engines(self)`
- `num_ready(self)`

## Dependencies

**Imports** (11):
- `Config.EngineIdentity`
- `Config.EngineState`
- `Config.LoadBalancingStrategy`
- `Config.ParallelConfig`
- `Messages.MetricsMessage`
- `__future__.annotations`
- `logging`
- `numpy`
- `threading`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
