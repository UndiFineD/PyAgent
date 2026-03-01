# utils

**File**: `src\infrastructure\moe\fused\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 4 imports  
**Lines**: 64  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for utils.

## Functions (2)

### `determine_expert_map(ep_size, ep_rank, global_num_experts, strategy, num_fused_shared_experts)`

Calculate expert assignment for expert parallelism.

### `get_compressed_expert_map(expert_map)`

Compress expert map to string for logging.

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `config.ExpertPlacementStrategy`
- `numpy`
- `rust_core`

---
*Auto-generated documentation*
