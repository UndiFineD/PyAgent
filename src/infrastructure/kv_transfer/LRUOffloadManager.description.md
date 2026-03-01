# LRUOffloadManager

**File**: `src\infrastructure\kv_transfer\LRUOffloadManager.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 24 imports  
**Lines**: 545  
**Complexity**: 28 (complex)

## Overview

LRUOffloadManager: LRU-based KV Cache Offloading

Implements simple LRU (Least Recently Used) eviction policy
for KV cache offloading with optimizations for batch operations.

Key Features Beyond vLLM:
- Weighted LRU with size and access frequency factors
- Batch eviction optimization
- Prefetch hints integration
- Multi-tier LRU (hot/warm/cold)
- Async batch operations

Based on vLLM v1 patterns with PyAgent innovations.

## Classes (7)

### `LRUEntry`

Entry in LRU cache with metadata.

**Methods** (1):
- `priority(self)`

### `LRUOffloadManager`

**Inherits from**: OffloadingManager

LRU-based offloading manager.

Simple but effective LRU eviction policy for KV cache offloading.
Evicts least recently used blocks when space is needed.

**Methods** (9):
- `__init__(self, backend, enable_events)`
- `lookup(self, block_hashes)`
- `prepare_load(self, block_hashes)`
- `touch(self, block_hashes)`
- `complete_load(self, block_hashes)`
- `prepare_store(self, block_hashes)`
- `complete_store(self, block_hashes)`
- `get_stats(self)`
- `clear(self)`

### `WeightedLRUManager`

**Inherits from**: LRUOffloadManager

Weighted LRU with access frequency consideration.

Combines recency with access frequency for smarter eviction.

**Methods** (3):
- `__init__(self, backend, enable_events, frequency_weight)`
- `touch(self, block_hashes)`
- `prepare_store(self, block_hashes)`

### `TieredLRUManager`

Multi-tier LRU manager with hot/warm/cold tiers.

Blocks are promoted through tiers based on access patterns.

**Methods** (6):
- `__init__(self, hot_backend, warm_backend, cold_backend, hot_ratio, warm_ratio)`
- `lookup(self, block_hashes)`
- `touch(self, block_hashes)`
- `_promote(self, block_hash, from_manager, to_manager)`
- `prepare_store(self, block_hashes)`
- `get_stats(self)`

### `PrefetchingLRUManager`

**Inherits from**: LRUOffloadManager

LRU manager with prefetching support.

Maintains prefetch hints to proactively load blocks.

**Methods** (4):
- `__init__(self, backend, enable_events, prefetch_lookahead)`
- `hint_prefetch(self, block_hashes)`
- `process_prefetch(self)`
- `complete_prefetch(self, block_hashes)`

### `AsyncLRUManager`

Async wrapper for LRU offloading manager.

**Methods** (1):
- `__init__(self, manager)`

### `LRUManagerFactory`

Factory for creating LRU managers.

**Methods** (4):
- `create_simple(num_blocks, block_size)`
- `create_weighted(num_blocks, block_size, frequency_weight)`
- `create_tiered(hot_blocks, warm_blocks, cold_blocks, block_size)`
- `create_prefetching(num_blocks, block_size, prefetch_lookahead)`

## Dependencies

**Imports** (24):
- `__future__.annotations`
- `asyncio`
- `collections.OrderedDict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `heapq`
- `rust_core`
- `src.infrastructure.kv_transfer.ARCOffloadManager.Backend`
- `src.infrastructure.kv_transfer.ARCOffloadManager.BlockHash`
- `src.infrastructure.kv_transfer.ARCOffloadManager.BlockState`
- `src.infrastructure.kv_transfer.ARCOffloadManager.BlockStatus`
- `src.infrastructure.kv_transfer.ARCOffloadManager.LoadStoreSpec`
- `src.infrastructure.kv_transfer.ARCOffloadManager.OffloadMedium`
- `src.infrastructure.kv_transfer.ARCOffloadManager.OffloadingEvent`
- `src.infrastructure.kv_transfer.ARCOffloadManager.OffloadingManager`
- ... and 9 more

---
*Auto-generated documentation*
