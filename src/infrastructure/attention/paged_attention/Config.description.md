# Config

**File**: `src\infrastructure\attention\paged_attention\Config.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 40  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for Config.

## Classes (1)

### `AttentionConfig`

Configuration for attention computation.

**Methods** (4):
- `__post_init__(self)`
- `num_queries_per_kv(self)`
- `is_gqa(self)`
- `is_mqa(self)`

## Dependencies

**Imports** (7):
- `Enums.KVCacheDtype`
- `__future__.annotations`
- `dataclasses.dataclass`
- `math`
- `numpy`
- `numpy.typing.NDArray`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
