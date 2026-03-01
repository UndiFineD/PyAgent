# dispatcher

**File**: `src\infrastructure\moe\fused\dispatcher.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 6 imports  
**Lines**: 99  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for dispatcher.

## Classes (2)

### `SparseDispatcher`

Sparse dispatcher for token-to-expert assignment.

**Methods** (3):
- `__init__(self, num_experts, top_k, capacity_factor)`
- `dispatch(self, x, expert_indices, expert_weights)`
- `combine(self, expert_outputs, expert_positions, expert_weights_list, output_shape)`

### `DenseDispatcher`

Dense dispatcher using matrix operations.

**Methods** (2):
- `__init__(self, num_experts, top_k)`
- `dispatch_and_combine(self, x, expert_indices, expert_weights, expert_fn)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `numpy`
- `typing.Any`
- `typing.Callable`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
