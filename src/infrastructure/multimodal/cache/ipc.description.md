# ipc

**File**: `src\infrastructure\multimodal\cache\ipc.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 84  
**Complexity**: 8 (moderate)

## Overview

IPC-enabled multimodal cache.

## Classes (1)

### `IPCMultiModalCache`

**Inherits from**: MultiModalCache

IPC-enabled cache for cross-process sharing.

**Methods** (8):
- `__init__(self, name, max_size_bytes, max_entries, hasher, create)`
- `_initialize_shared(self)`
- `get(self, key)`
- `put(self, key, data, metadata)`
- `evict(self, count)`
- `clear(self)`
- `contains(self, key)`
- `share_entry(self, key)`

## Dependencies

**Imports** (9):
- `base.MultiModalCache`
- `data.CacheEntry`
- `data.MediaHash`
- `memory.MemoryMultiModalCache`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
