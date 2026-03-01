# data

**File**: `src\infrastructure\multimodal\cache\data.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 7 imports  
**Lines**: 72  
**Complexity**: 5 (moderate)

## Overview

Data structures for multimodal caching.

## Classes (4)

### `MediaHash`

Content hash for media items.

**Methods** (2):
- `__hash__(self)`
- `__eq__(self, other)`

### `CacheEntry`

Entry in the multimodal cache.

**Methods** (1):
- `touch(self)`

### `CacheStats`

Statistics for cache performance.

**Methods** (1):
- `hit_rate(self)`

### `PlaceholderRange`

Range of tokens for multimodal placeholder.

**Methods** (1):
- `length(self)`

## Dependencies

**Imports** (7):
- `dataclasses.dataclass`
- `dataclasses.field`
- `enums.HashAlgorithm`
- `enums.MediaType`
- `time`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
