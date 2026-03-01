# models

**File**: `src\infrastructure\distributed\tp\models.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 7 imports  
**Lines**: 112  
**Complexity**: 3 (simple)

## Overview

Models and configuration for tensor parallelism.

## Classes (3)

### `ParallelMode`

**Inherits from**: Enum

Parallelism modes.

### `ParallelConfig`

Configuration for distributed parallelism.

Defines the parallelism strategy across dimensions.

**Methods** (2):
- `__post_init__(self)`
- `from_env(cls)`

### `RankInfo`

Information about a rank's position in the parallel topology.

**Methods** (1):
- `compute(cls, global_rank, config)`

## Dependencies

**Imports** (7):
- `coordinator.GroupCoordinator`
- `dataclasses.dataclass`
- `enum.Enum`
- `enum.auto`
- `logging`
- `os`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
