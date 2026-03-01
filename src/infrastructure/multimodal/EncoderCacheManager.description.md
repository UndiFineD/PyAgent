# EncoderCacheManager

**File**: `src\infrastructure\multimodal\EncoderCacheManager.py`  
**Type**: Python Module  
**Summary**: 7 classes, 1 functions, 19 imports  
**Lines**: 645  
**Complexity**: 31 (complex)

## Overview

Encoder Cache Manager for Multimodal Models.

This module manages caching of encoder outputs (vision embeddings, audio features)
for multimodal LLM inference, avoiding redundant encoder computations.

Features beyond vLLM:
- Multi-tier caching (memory, disk, remote)
- Content-based deduplication via hashing
- Predictive prefetching
- Reference counting with weak references
- LRU eviction with priority support

## Classes (7)

### `CacheTier`

**Inherits from**: Enum

Cache storage tier.

### `EvictionPolicy`

**Inherits from**: Enum

Cache eviction policy.

### `CacheConfig`

Configuration for encoder cache.

**Methods** (1):
- `__post_init__(self)`

### `CacheEntry`

A single cache entry.

**Methods** (4):
- `touch(self)`
- `age_seconds(self)`
- `idle_seconds(self)`
- `is_referenced(self)`

### `CacheStats`

Cache statistics.

**Methods** (3):
- `hit_rate(self)`
- `bytes_cached_mb(self)`
- `reset(self)`

### `EncoderCacheManager`

Manages caching of encoder outputs for multimodal models.

Implements vLLM's EncoderCacheManager with extensions:
- Content-based deduplication
- Reference counting
- LRU/LFU/Priority eviction
- Prefetching support

**Methods** (17):
- `__init__(self, config)`
- `get(self, key, request_id)`
- `put(self, key, data, request_id, priority, content_hash)`
- `check_cached(self, key)`
- `release_request(self, request_id)`
- `compute_hash(self, data)`
- `prefetch(self, keys, loader)`
- `evict_unreferenced(self)`
- `clear(self)`
- `get_stats(self)`
- ... and 7 more methods

### `MultiTierEncoderCache`

Multi-tier encoder cache with memory, disk, and remote tiers.

Beyond vLLM: Hierarchical caching with automatic tier migration
and consistent access patterns.

**Methods** (5):
- `__init__(self, memory_config, disk_path, remote_url)`
- `get(self, key, request_id)`
- `put(self, key, data, request_id, tier)`
- `_load_from_disk(self, key)`
- `_save_to_disk(self, key, data)`

## Functions (1)

### `create_encoder_cache(cache_size, memory_mb, eviction, enable_dedup)`

Factory function to create encoder cache.

Args:
    cache_size: Maximum number of entries
    memory_mb: Memory budget in MB
    eviction: "lru", "lfu", "fifo", "priority"
    enable_dedup: Enable content deduplication
    **kwargs: Additional config options

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `collections.OrderedDict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `hashlib`
- `numpy`
- `numpy.typing.NDArray`
- `os`
- `rust_core`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Generic`
- ... and 4 more

---
*Auto-generated documentation*
