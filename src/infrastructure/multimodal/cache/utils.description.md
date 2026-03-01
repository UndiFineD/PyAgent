# utils

**File**: `src\infrastructure\multimodal\cache\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 13 imports  
**Lines**: 62  
**Complexity**: 2 (simple)

## Overview

Utility functions for multimodal caching.

## Functions (2)

### `compute_media_hash(data, media_type, algorithm)`

Compute hash for media content.

### `create_cache(backend, max_size_bytes, max_entries)`

Factory function to create cache instance.

## Dependencies

**Imports** (13):
- `base.MultiModalCache`
- `data.MediaHash`
- `enums.CacheBackend`
- `enums.HashAlgorithm`
- `enums.MediaType`
- `hasher.HAS_PIL`
- `hasher.MultiModalHasher`
- `ipc.IPCMultiModalCache`
- `memory.MemoryMultiModalCache`
- `numpy`
- `typing.Any`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
