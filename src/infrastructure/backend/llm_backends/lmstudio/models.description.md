# models

**File**: `src\infrastructure\backend\llm_backends\lmstudio\models.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 5 imports  
**Lines**: 59  
**Complexity**: 3 (simple)

## Overview

Models and configuration for LM Studio backend.

## Classes (2)

### `LMStudioConfig`

Configuration for LM Studio connection.

**Methods** (1):
- `api_host(self)`

### `CachedModel`

Cached model reference with TTL.

**Methods** (2):
- `is_expired(self, ttl)`
- `touch(self)`

## Dependencies

**Imports** (5):
- `dataclasses.dataclass`
- `dataclasses.field`
- `os`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
