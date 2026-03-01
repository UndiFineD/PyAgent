# KVCacheManager

**File**: `src\infrastructure\cache\KVCacheManager.py`  
**Type**: Python Module  
**Summary**: 9 classes, 1 functions, 12 imports  
**Lines**: 534  
**Complexity**: 40 (complex)

## Overview

KV Cache Manager.

GPU/CPU KV cache orchestration for transformer inference:
- Paged attention memory layout
- Block allocation and defragmentation
- CPU-GPU tensor transfers

Inspired by vLLM's v1/core/kv_cache_manager.py architecture.

## Classes (9)

### `DeviceType`

**Inherits from**: str, Enum

Device type for KV cache.

### `DType`

**Inherits from**: str, Enum

Data type for KV cache.

### `KVCacheConfig`

Configuration for KV cache.

**Methods** (2):
- `kv_size_per_token(self)`
- `block_size_bytes(self)`

### `KVCacheBlock`

A block in the KV cache.

**Methods** (4):
- `allocate(self, num_heads, head_dim, block_size, dtype)`
- `free(self)`
- `acquire(self)`
- `release(self)`

### `KVCacheBlocks`

Collection of KV cache blocks for a request.

**Methods** (3):
- `num_blocks(self)`
- `append_gpu(self, block_id)`
- `append_cpu(self, block_id)`

### `KVCacheAllocator`

Allocates and manages KV cache blocks.

Supports paged attention memory layout with block pooling.

**Methods** (8):
- `__init__(self, config)`
- `_init_pools(self)`
- `allocate_gpu_block(self, layer_idx)`
- `allocate_cpu_block(self, layer_idx)`
- `free_block(self, block)`
- `get_num_free_gpu_blocks(self)`
- `get_num_free_cpu_blocks(self)`
- `usage(self)`

### `PagedKVCache`

Paged KV cache with block-level management.

Supports efficient memory utilization through paging.

**Methods** (8):
- `__init__(self, config)`
- `allocate_for_request(self, request_id, num_tokens)`
- `extend_allocation(self, request_id, additional_tokens)`
- `_get_block_tokens(self, request_id, layer_idx, block_id)`
- `free_request(self, request_id)`
- `get_block_table(self, request_id, layer_idx)`
- `usage(self)`
- `get_num_free_blocks(self)`

### `KVCacheTransfer`

Manages CPU-GPU tensor transfers for KV cache swapping.

**Methods** (4):
- `__init__(self, config)`
- `swap_out(self, gpu_block, cpu_block)`
- `swap_in(self, cpu_block, gpu_block)`
- `copy_blocks(self, src_blocks, dst_blocks)`

### `KVCacheManager`

Main KV cache manager coordinating allocation, caching, and transfers.

**Methods** (10):
- `__init__(self, config)`
- `allocate(self, request_id, num_tokens)`
- `extend(self, request_id, additional_tokens)`
- `free(self, request_id)`
- `get_block_table(self, request_id, layer_idx)`
- `usage(self)`
- `get_num_free_blocks(self)`
- `can_allocate(self, num_tokens)`
- `on_memory_pressure(self, callback)`
- `_trigger_memory_pressure(self)`

## Functions (1)

### `create_kv_cache_manager(num_layers, num_heads, head_dim, num_blocks, block_size)`

Create a KV cache manager.

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `numpy`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Generic`
- `typing.Protocol`
- `typing.TypeVar`

---
*Auto-generated documentation*
