# DataClasses

**File**: `src\infrastructure\engine\kv_cache\DataClasses.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 11 imports  
**Lines**: 126  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for DataClasses.

## Classes (6)

### `BlockHash`

Immutable block hash for prefix caching.

**Methods** (3):
- `__hash__(self)`
- `__eq__(self, other)`
- `as_int(self)`

### `BlockHashWithGroupId`

Block hash combined with group ID for multi-group caching.

**Methods** (1):
- `__hash__(self)`

### `KVCacheBlock`

KV cache block metadata.

**Methods** (2):
- `touch(self)`
- `reset(self)`

### `KVCacheBlocks`

Allocation result for multi-group KV cache.

**Methods** (4):
- `__add__(self, other)`
- `get_block_ids(self)`
- `is_empty(self)`
- `empty(cls, num_groups)`

### `CacheGroupSpec`

Specification for a KV cache group.

**Methods** (2):
- `bytes_per_token(self)`
- `bytes_per_block(self)`

### `CacheConfig`

Configuration for KV cache.

## Dependencies

**Imports** (11):
- `Enums.AllocationStrategy`
- `Enums.CacheGroupType`
- `Enums.EvictionPolicy`
- `dataclasses.dataclass`
- `dataclasses.field`
- `time`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Sequence`
- `typing.Tuple`

---
*Auto-generated documentation*
