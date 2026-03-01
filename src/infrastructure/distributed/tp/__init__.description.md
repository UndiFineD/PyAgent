# __init__

**File**: `src\infrastructure\distributed\tp\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 7 imports  
**Lines**: 79  
**Complexity**: 4 (simple)

## Overview

Tensor parallel coordination for distributed inference.

## Functions (4)

### `init_distributed(config, rank)`

Initialize distributed tensor parallelism.

Args:
    config: Parallel configuration (uses env vars if None)
    rank: Global rank (uses env var if None)
    
Returns:
    TensorParallelGroup for collective operations

### `get_tp_group()`

Get the global tensor parallel group.

### `get_tp_size()`

Get tensor parallel world size.

### `get_tp_rank()`

Get tensor parallel rank.

## Dependencies

**Imports** (7):
- `coordinator.GroupCoordinator`
- `group.TensorParallelGroup`
- `models.ParallelConfig`
- `models.ParallelMode`
- `models.RankInfo`
- `os`
- `typing.Optional`

---
*Auto-generated documentation*
