# Ops

**File**: `src\infrastructure\attention\paged_attention\Ops.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 74  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for Ops.

## Classes (1)

### `PagedAttentionOps`

Pure NumPy implementation of paged attention operations.

**Methods** (4):
- `scaled_dot_product_attention(query, key, value, scale, causal, sliding_window)`
- `paged_attention_v1(query, key_cache, block_tables, seq_lens, config)`
- `paged_attention_v2(query, key_cache, block_tables, seq_lens, config, partition_size)`
- `expand_kv_for_gqa(kv, num_queries_per_kv)`

## Dependencies

**Imports** (3):
- `Config.AttentionConfig`
- `Storage.PagedKVCache`
- `numpy`

---
*Auto-generated documentation*
