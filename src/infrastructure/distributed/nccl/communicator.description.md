# communicator

**File**: `src\infrastructure\distributed\nccl\communicator.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 10 imports  
**Lines**: 477  
**Complexity**: 22 (complex)

## Overview

NCCL communicator and custom operations.

## Classes (2)

### `NCCLCommunicator`

Pure Python wrapper for NCCL collective operations.

Provides:
- Standard collective operations with error handling
- Automatic retry on transient failures
- Stream-based async operations
- CUDA graph compatibility

**Methods** (18):
- `__init__(self, group, config, device)`
- `world_size(self)`
- `rank(self)`
- `_map_reduce_op(self, op)`
- `_with_retry(self, op_name, fn)`
- `_timed_op(self, op_name, tensor)`
- `all_reduce(self, tensor, op, async_op)`
- `all_gather(self, tensor, dim, async_op)`
- `reduce_scatter(self, tensor, dim, op, async_op)`
- `reduce_scatterv(self, tensor, output_sizes, dim, op)`
- ... and 8 more methods

### `CustomAllReduce`

Custom all-reduce implementation for specific scenarios.

**Methods** (4):
- `__init__(self, communicator, threshold)`
- `all_reduce(self, tensor, op)`
- `_custom_all_reduce(self, tensor, op)`
- `get_stats(self)`

## Dependencies

**Imports** (10):
- `contextlib.contextmanager`
- `logging`
- `models.NCCLConfig`
- `models.NCCLStats`
- `models.ReduceOp`
- `time`
- `torch`
- `torch.distributed`
- `typing.Any`
- `typing.Callable`

---
*Auto-generated documentation*
