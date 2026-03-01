# balancer

**File**: `src\infrastructure\parallel\dp\balancer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 64  
**Complexity**: 3 (simple)

## Overview

Load balancing strategies for Data Parallel coordination.

## Classes (1)

### `P2CLoadBalancer`

Power of Two Choices load balancer.

**Methods** (3):
- `__init__(self, workers, sample_size, enable_locality)`
- `select_worker(self, locality_group)`
- `update_workers(self, workers)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `random`
- `src.infrastructure.parallel.dp.types.WorkerHealth`
- `src.infrastructure.parallel.dp.types.WorkerState`
- `threading`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
