# memory

**File**: `src\infrastructure\multimodal\cache\memory.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 13 imports  
**Lines**: 233  
**Complexity**: 15 (moderate)

## Overview

In-memory and specialized multimodal cache implementations.

## Classes (3)

### `MemoryMultiModalCache`

**Inherits from**: MultiModalCache

In-memory LRU cache for multimodal content.

**Methods** (7):
- `__init__(self, max_size_bytes, max_entries, hasher)`
- `get(self, key)`
- `put(self, key, data, metadata)`
- `evict(self, count)`
- `clear(self)`
- `contains(self, key)`
- `keys(self)`

### `PerceptualCache`

**Inherits from**: MemoryMultiModalCache

Cache with perceptual similarity matching.

**Methods** (3):
- `__init__(self, max_size_bytes, max_entries, similarity_threshold)`
- `put_with_perceptual(self, content_hash, data, perceptual_hash, metadata)`
- `find_similar(self, perceptual_hash)`

### `PrefetchMultiModalCache`

**Inherits from**: MemoryMultiModalCache

Cache with async prefetch support.

**Methods** (5):
- `__init__(self, max_size_bytes, max_entries, max_prefetch_queue)`
- `record_access(self, key, subsequent_key)`
- `predict_next(self, key)`
- `schedule_prefetch(self, key, loader, priority)`
- `execute_prefetch(self, count)`

## Dependencies

**Imports** (13):
- `base.MultiModalCache`
- `collections.Counter`
- `collections.OrderedDict`
- `data.CacheEntry`
- `data.MediaHash`
- `numpy`
- `threading`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
