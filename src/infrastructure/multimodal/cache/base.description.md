# base

**File**: `src\infrastructure\multimodal\cache\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 77  
**Complexity**: 8 (moderate)

## Overview

Base class for multimodal caching.

## Classes (1)

### `MultiModalCache`

**Inherits from**: ABC

Abstract base for multimodal content caching.

Features:
- LRU eviction with configurable capacity
- Content-aware hashing
- Statistics tracking

**Methods** (8):
- `__init__(self, max_size_bytes, max_entries, hasher)`
- `get(self, key)`
- `put(self, key, data, metadata)`
- `evict(self, count)`
- `clear(self)`
- `contains(self, key)`
- `get_or_compute(self, key, compute_fn, metadata)`
- `stats(self)`

## Dependencies

**Imports** (11):
- `abc.ABC`
- `abc.abstractmethod`
- `data.CacheEntry`
- `data.CacheStats`
- `data.MediaHash`
- `hasher.MultiModalHasher`
- `threading`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
