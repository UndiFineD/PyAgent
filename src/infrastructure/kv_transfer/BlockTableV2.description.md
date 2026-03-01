# BlockTableV2

**File**: `src\infrastructure\kv_transfer\BlockTableV2.py`  
**Type**: Python Module  
**Summary**: 10 classes, 0 functions, 11 imports  
**Lines**: 635  
**Complexity**: 44 (complex)

## Overview

BlockTableV2: Enhanced Block Table Management

Provides efficient block table management for KV cache with
hybrid block sizes, slot mapping, and distributed support.

Key Features Beyond vLLM:
- Dynamic block size adaptation
- Compressed slot mappings
- Multi-GPU block coordination
- Predictive block allocation
- Memory-efficient sparse tables

Based on vLLM v1 patterns with PyAgent innovations.

## Classes (10)

### `BlockAllocationStrategy`

**Inherits from**: Enum

Strategy for block allocation.

### `BlockTableConfig`

Configuration for block table.

### `BlockInfo`

Information about a block.

**Methods** (3):
- `increment_ref(self)`
- `decrement_ref(self)`
- `can_free(self)`

### `CpuGpuBuffer`

Buffer that syncs between CPU and GPU.

**Methods** (7):
- `__init__(self, shape, dtype)`
- `get_cpu(self)`
- `get_gpu(self)`
- `set(self, row, col, value)`
- `get(self, row, col)`
- `_sync_to_gpu(self)`
- `set_row(self, row, values)`

### `BlockTable`

Block table for managing KV cache block mappings.

Maps sequence positions to physical memory blocks for
efficient KV cache access during attention computation.

**Methods** (9):
- `__init__(self, config)`
- `append_row(self, row_idx, block_ids, num_tokens)`
- `get_row(self, row_idx)`
- `clear_row(self, row_idx)`
- `compute_slot_mapping(self, row_idx, num_tokens, start_position)`
- `update_slot_mapping(self, token_positions)`
- `_compute_single_slot(self, row_idx, position)`
- `get_num_blocks(self, row_idx)`
- `get_total_blocks(self)`

### `SparseBlockTable`

Sparse block table for memory-efficient storage.

Uses sparse representation for requests with few blocks.

**Methods** (6):
- `__init__(self, config)`
- `set_block(self, row_idx, position, block_id)`
- `get_block(self, row_idx, position)`
- `get_slot(self, row_idx, position)`
- `clear_row(self, row_idx)`
- `to_dense(self, row_idx, max_blocks)`

### `PredictiveBlockAllocator`

Block allocator with predictive pre-allocation.

Predicts future block needs based on sequence patterns.

**Methods** (5):
- `__init__(self, total_blocks, block_size, prediction_horizon)`
- `allocate(self, request_id, num_blocks, predict_future)`
- `free(self, block_ids)`
- `_predict_future_need(self, request_id)`
- `get_num_free(self)`

### `DistributedBlockTable`

Block table with distributed coordination.

Coordinates block allocation across multiple GPUs/workers.

**Methods** (4):
- `__init__(self, config, num_workers, worker_id)`
- `allocate_blocks(self, row_idx, num_blocks, prefer_local)`
- `get_block_location(self, block_id)`
- `is_local(self, block_id)`

### `BlockTableV2`

Enhanced block table with all advanced features.

Combines standard, sparse, predictive, and distributed features.

**Methods** (7):
- `__init__(self, config, use_sparse, use_prediction)`
- `append_row(self, row_idx, block_ids, num_tokens)`
- `get_row(self, row_idx)`
- `clear_row(self, row_idx)`
- `compute_slot_mapping(self, row_idx, num_tokens, start_position)`
- `allocate_for_request(self, request_id, row_idx, num_blocks)`
- `get_stats(self)`

### `BlockTableFactory`

Factory for creating block tables.

**Methods** (3):
- `create_standard(block_size, max_num_reqs, max_blocks_per_req)`
- `create_sparse(block_size)`
- `create_v2(block_size, use_sparse, use_prediction)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `math`
- `rust_core`
- `threading`
- `time`
- `typing.Any`
- `typing.Protocol`

---
*Auto-generated documentation*
