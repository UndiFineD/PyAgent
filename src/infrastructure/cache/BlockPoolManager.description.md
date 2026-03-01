# BlockPoolManager

**File**: `src\infrastructure\cache\BlockPoolManager.py`  
**Type**: Python Module  
**Summary**: 8 classes, 1 functions, 14 imports  
**Lines**: 558  
**Complexity**: 29 (complex)

## Overview

BlockPoolManager: Advanced KV block pool management with LRU/ARC eviction.

vLLM Pattern: BlockPool from v1/core/block_pool.py
- get_new_blocks() / free_blocks() / cache_blocks() / touch()
- cached_block_hash_to_block for prefix cache lookup
- KVCacheMetricsCollector for eviction events

Beyond vLLM:
- ARC (Adaptive Replacement Cache) policy for better hit rates
- Block priority levels (PINNED > CACHED > ALLOCATED > FREE)
- Detailed eviction metrics and residency tracking

## Classes (8)

### `BlockState`

**Inherits from**: IntEnum

Block allocation state with priority ordering.

### `Block`

A single KV cache block.

**Methods** (1):
- `touch(self)`

### `BlockPoolConfig`

Configuration for block pool.

### `EvictionEvent`

Record of a block eviction.

### `CacheMetrics`

KV cache metrics.

**Methods** (1):
- `hit_rate(self)`

### `KVCacheMetricsCollector`

Collector for KV cache metrics.

vLLM Pattern: KVCacheMetricsCollector from block_pool.py

**Methods** (5):
- `__init__(self, pool)`
- `record_eviction(self, event)`
- `get_metrics(self)`
- `get_recent_evictions(self, limit)`
- `get_eviction_rate(self, window_seconds)`

### `ARCPolicy`

Adaptive Replacement Cache eviction policy.

Beyond vLLM: ARC balances recency (LRU) and frequency (LFU).

T1: Recent items (LRU of items seen once)
T2: Frequent items (LRU of items seen more than once)
B1: Ghost entries for recently evicted from T1
B2: Ghost entries for recently evicted from T2

Parameter p: Target size of T1 (adapts based on hit patterns)

**Methods** (6):
- `__init__(self, capacity, p_initial)`
- `access(self, block)`
- `insert(self, block)`
- `_evict(self)`
- `remove(self, block_id)`
- `get_stats(self)`

### `BlockPool`

Block pool with LRU/ARC eviction and prefix caching.

vLLM Pattern: BlockPool from v1/core/block_pool.py

**Methods** (15):
- `__init__(self, config)`
- `get_new_blocks(self, num_blocks)`
- `free_blocks(self, block_ids)`
- `cache_blocks(self, block_ids, block_hashes)`
- `touch(self, block_ids)`
- `lookup_cached_block(self, block_hash)`
- `pin_blocks(self, block_ids)`
- `unpin_blocks(self, block_ids)`
- `_evict_cached_blocks(self, num_needed)`
- `_handle_eviction(self, block_id, reason)`
- ... and 5 more methods

## Functions (1)

### `compute_block_hash(content)`

Compute hash for block content.

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `collections.OrderedDict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.IntEnum`
- `enum.auto`
- `hashlib`
- `logging`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Hashable`
- `typing.Optional`

---
*Auto-generated documentation*
