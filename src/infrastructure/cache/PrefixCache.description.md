# PrefixCache

**File**: `src\infrastructure\cache\PrefixCache.py`  
**Type**: Python Module  
**Summary**: 6 classes, 3 functions, 12 imports  
**Lines**: 456  
**Complexity**: 32 (complex)

## Overview

Prefix Cache System.

Hash-based content-addressable caching for LLM inference:
- Block-level caching with reference counting
- LRU/LFU/ARC eviction policies
- Cache statistics and monitoring

Inspired by vLLM's v1/core/kv_cache_utils.py architecture.

## Classes (6)

### `EvictionPolicy`

**Inherits from**: str, Enum

Cache eviction policy.

### `PrefixCacheConfig`

Configuration for prefix cache.

### `CacheBlock`

A cached block of tokens.

**Methods** (4):
- `touch(self)`
- `acquire(self)`
- `release(self)`
- `is_freeable(self)`

### `PrefixCacheStats`

Statistics for prefix cache performance.

**Methods** (4):
- `record(self, num_tokens, num_hits, preempted)`
- `hit_rate(self)`
- `reset(self)`
- `as_dict(self)`

### `PrefixCacheManager`

Manages prefix cache with hash-based content addressing.

Supports block sharing across requests with same prefix.

**Methods** (18):
- `__init__(self, config)`
- `num_blocks(self)`
- `num_free_blocks(self)`
- `usage(self)`
- `allocate_blocks(self, request_id, token_ids)`
- `_allocate_block(self, token_ids, block_hash)`
- `_update_access(self, block_id)`
- `_evict_one(self)`
- `_arc_evict(self)`
- `_free_block(self, block_id)`
- ... and 8 more methods

### `BlockHasher`

Configurable block hasher.

**Methods** (3):
- `__init__(self, algorithm)`
- `hash(self, token_ids)`
- `hash_bytes(self, data)`

## Functions (3)

### `compute_block_hash(token_ids, algorithm)`

Compute hash for a block of tokens.

### `create_prefix_cache(block_size, max_blocks, eviction_policy)`

Create a prefix cache manager.

### `get_request_block_hasher(algorithm)`

Get a block hasher instance.

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `collections.OrderedDict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `hashlib`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Generic`
- `typing.TypeVar`
- `xxhash`

---
*Auto-generated documentation*
