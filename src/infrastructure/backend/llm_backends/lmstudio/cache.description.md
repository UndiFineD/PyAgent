# cache

**File**: `src\infrastructure\backend\llm_backends\lmstudio\cache.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 49  
**Complexity**: 5 (moderate)

## Overview

Model cache for LM Studio handles.

## Classes (1)

### `ModelCache`

Simple model cache with TTL.

**Methods** (5):
- `__init__(self, ttl)`
- `get(self, model_id)`
- `set(self, model_id, model_info)`
- `clear(self)`
- `prune_expired(self)`

## Dependencies

**Imports** (3):
- `models.CachedModel`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
