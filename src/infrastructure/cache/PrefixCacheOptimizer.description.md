# PrefixCacheOptimizer

**File**: `src\infrastructure\cache\PrefixCacheOptimizer.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 15 imports  
**Lines**: 580  
**Complexity**: 22 (complex)

## Overview

PrefixCacheOptimizer: Prefix cache hit optimization with radix tree.

vLLM Pattern: KVCacheManager.find_longest_cache_hit() from kv_cache_manager.py
- get_computed_blocks() for cache hit detection
- remove_skipped_blocks() for memory reclamation

Beyond vLLM:
- Radix tree for O(log n) prefix matching
- Speculative prefix pre-warming
- Multi-tier cache (L1 hot, L2 warm, L3 cold)

## Classes (7)

### `CacheTier`

**Inherits from**: Enum

Cache tier for multi-level caching.

### `PrefixCacheConfig`

Configuration for prefix cache.

### `PrefixEntry`

An entry in the prefix cache.

**Methods** (1):
- `touch(self)`

### `CacheHitResult`

Result of a cache hit lookup.

### `RadixTreeNode`

Node in a radix tree for prefix matching.

Each node represents a sequence of tokens.

**Methods** (2):
- `__init__(self, prefix)`
- `__repr__(self)`

### `PrefixTree`

Radix tree for efficient prefix matching.

Beyond vLLM: O(log n) prefix matching vs linear scan.

**Methods** (5):
- `__init__(self)`
- `insert(self, tokens, entry)`
- `find_longest_prefix(self, tokens)`
- `remove(self, tokens)`
- `__len__(self)`

### `PrefixCacheOptimizer`

Prefix cache with radix tree lookup and multi-tier caching.

vLLM Pattern: KVCacheManager prefix caching

Beyond vLLM:
- Radix tree for O(log n) prefix matching
- Speculative prefix pre-warming
- Multi-tier caching (hot/warm/cold)

**Methods** (14):
- `__init__(self, config)`
- `cache_prefix(self, token_ids, block_ids, metadata)`
- `find_longest_cache_hit(self, token_ids)`
- `get_computed_blocks(self, token_ids)`
- `remove_skipped_blocks(self, block_ids)`
- `update_prefix_state(self, prefix_hash, new_block_ids)`
- `_compute_hash(self, tokens)`
- `_update_tier(self, entry)`
- `_track_prewarm_candidate(self, prefix_hash)`
- `_evict_batch(self)`
- ... and 4 more methods

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `hashlib`
- `logging`
- `threading`
- `time`
- `typing.Any`
- `typing.Generic`
- `typing.Hashable`
- `typing.Optional`
- `typing.Sequence`
- `typing.TypeVar`

---
*Auto-generated documentation*
