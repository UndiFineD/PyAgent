# Engine

**File**: `src\infrastructure\attention\paged_attention\Engine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 1 functions, 9 imports  
**Lines**: 64  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for Engine.

## Classes (1)

### `PagedAttentionEngine`

Class PagedAttentionEngine implementation.

**Methods** (6):
- `__init__(self, config, num_blocks)`
- `allocate_sequence(self, seq_id, initial_len)`
- `append_kv(self, seq_id, key, value)`
- `forward(self, query, seq_ids, use_v2)`
- `free_sequence(self, seq_id)`
- `get_stats(self)`

## Functions (1)

### `create_attention_engine(head_size, num_heads, num_kv_heads, block_size, num_blocks)`

## Dependencies

**Imports** (9):
- `Config.AttentionConfig`
- `Enums.KVCacheDtype`
- `Ops.PagedAttentionOps`
- `Storage.BlockTable`
- `Storage.PagedKVCache`
- `Storage.SlotMapping`
- `numpy`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
