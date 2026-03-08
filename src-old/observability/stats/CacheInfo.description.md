# CacheInfo

**File**: `src\observability\stats\CacheInfo.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 11 imports  
**Lines**: 417  
**Complexity**: 30 (complex)

## Overview

CacheInfo - LRU Cache with hit/miss statistics and pinned items.

Inspired by vLLM's cache.py patterns for production cache monitoring.

Phase 17: vLLM Pattern Integration

## Classes (4)

### `CacheStats`

Statistics for cache performance monitoring.

**Methods** (5):
- `total(self)`
- `hit_ratio(self)`
- `miss_ratio(self)`
- `reset(self)`
- `to_dict(self)`

### `CacheEntry`

**Inherits from**: Unknown

A cache entry with value, timestamp, and pin status.

**Methods** (1):
- `touch(self)`

### `LRUCache`

**Inherits from**: Unknown

Thread-safe LRU cache with hit statistics and pinned items.

Features:
- Hit/miss tracking with statistics
- Pinned items that won't be evicted
- Delta statistics (changes since last check)
- Touch operation for manual LRU updates
- Capacity tracking

Example:
    >>> cache = LRUCache[str, int](max_size=100)
    >>> cache.put("key1", 42)
    >>> value = cache.get("key1")  # Returns 42, records hit
    >>> value = cache.get("key2")  # Returns None, records miss
    >>> print(cache.stats.hit_ratio)  # 0.5

**Methods** (23):
- `__init__(self, max_size, ttl_seconds, name)`
- `stats(self)`
- `size(self)`
- `capacity(self)`
- `usage(self)`
- `get(self, key, default)`
- `put(self, key, value, pinned)`
- `touch(self, key)`
- `pin(self, key)`
- `unpin(self, key)`
- ... and 13 more methods

### `TTLLRUCache`

**Inherits from**: Unknown

LRU Cache with mandatory TTL.

Convenience class for caches that always need TTL.

**Methods** (1):
- `__init__(self, max_size, ttl_seconds, name)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `collections.OrderedDict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `threading`
- `time`
- `typing.Generic`
- `typing.Hashable`
- `typing.Iterator`
- `typing.Optional`
- `typing.TypeVar`

---
*Auto-generated documentation*
