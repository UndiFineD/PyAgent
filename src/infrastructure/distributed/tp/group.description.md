# group

**File**: `src\infrastructure\distributed\tp\group.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 323  
**Complexity**: 15 (moderate)

## Overview

Tensor parallel group operations.

## Classes (1)

### `TensorParallelGroup`

Tensor parallel operations for distributed model execution.

Provides collective operations (all_reduce, all_gather, etc.)
specifically for tensor parallelism.

**Methods** (15):
- `__init__(self, coordinator, device)`
- `tp_size(self)`
- `tp_rank(self)`
- `is_first_rank(self)`
- `is_last_rank(self)`
- `all_reduce(self, tensor, op, async_op)`
- `all_gather(self, tensor, dim, async_op)`
- `reduce_scatter(self, tensor, dim, op, async_op)`
- `scatter(self, tensor, dim, src_rank)`
- `broadcast(self, tensor, src_rank, async_op)`
- ... and 5 more methods

## Dependencies

**Imports** (6):
- `contextlib.contextmanager`
- `coordinator.GroupCoordinator`
- `logging`
- `torch`
- `torch.distributed`
- `typing.Any`

---
*Auto-generated documentation*
