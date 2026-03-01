# Config

**File**: `src\infrastructure\orchestration\core\distributed\Config.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 6 imports  
**Lines**: 115  
**Complexity**: 3 (simple)

## Overview

Configuration and state enums for distributed coordination.

## Classes (6)

### `EngineState`

**Inherits from**: Enum

State of a distributed engine instance.

### `WorkerState`

**Inherits from**: Enum

State of a worker process.

### `LoadBalancingStrategy`

**Inherits from**: Enum

Load balancing strategies for data parallel.

### `ParallelConfig`

Configuration for parallelism.

Inspired by vLLM's ParallelConfig.

Attributes:
    data_parallel_size: Number of data parallel replicas.
    tensor_parallel_size: Number of tensor parallel ranks.
    pipeline_parallel_size: Number of pipeline stages.
    world_size: Total number of distributed ranks.
    distributed_executor_backend: Backend type (mp, ray).
    worker_use_ray: Whether workers use Ray.
    max_parallel_loading: Max workers loading simultaneously.

**Methods** (2):
- `world_size(self)`
- `is_distributed(self)`

### `EngineIdentity`

Identity of a distributed engine instance.

Inspired by vLLM's coordinator identity management.

Attributes:
    dp_rank: Data parallel rank.
    dp_size: Data parallel world size.
    address: Network address.
    engine_id: Unique engine identifier.

**Methods** (1):
- `__str__(self)`

### `WorkerIdentity`

Identity of a worker process.

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `uuid`

---
*Auto-generated documentation*
