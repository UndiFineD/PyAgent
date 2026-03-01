# engine

**File**: `src\infrastructure\parallel\dp\engine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 15 imports  
**Lines**: 229  
**Complexity**: 18 (moderate)

## Overview

Engine core processor for data parallel coordination.

## Classes (1)

### `DPEngineCoreProc`

Data Parallel engine core processor.

**Methods** (18):
- `__init__(self, config)`
- `_init_workers(self)`
- `begin_step(self, num_requests)`
- `end_step(self)`
- `step_sync(self)`
- `begin_wave(self, num_steps)`
- `wave_complete(self)`
- `end_wave(self)`
- `wave_sync(self)`
- `select_worker(self, locality_group)`
- ... and 8 more methods

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `collections.deque`
- `logging`
- `src.infrastructure.parallel.dp.balancer.P2CLoadBalancer`
- `src.infrastructure.parallel.dp.types.DPConfig`
- `src.infrastructure.parallel.dp.types.StepState`
- `src.infrastructure.parallel.dp.types.WaveState`
- `src.infrastructure.parallel.dp.types.WorkerHealth`
- `src.infrastructure.parallel.dp.types.WorkerState`
- `threading`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
