# coordinator

**File**: `src\infrastructure\distributed\tp\coordinator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 184  
**Complexity**: 11 (moderate)

## Overview

Process group coordinator for distributed operations.

## Classes (1)

### `GroupCoordinator`

Manages process groups for distributed operations.

Creates and caches process groups for different parallelism modes.

**Methods** (11):
- `__init__(self, config, rank_info)`
- `initialize(self)`
- `_create_tp_group(self)`
- `_create_pp_group(self)`
- `_create_dp_group(self)`
- `world_group(self)`
- `tp_group(self)`
- `pp_group(self)`
- `dp_group(self)`
- `get_world_size(self, mode)`
- ... and 1 more methods

## Dependencies

**Imports** (7):
- `logging`
- `models.ParallelConfig`
- `models.ParallelMode`
- `models.RankInfo`
- `torch`
- `torch.distributed`
- `typing.Any`

---
*Auto-generated documentation*
