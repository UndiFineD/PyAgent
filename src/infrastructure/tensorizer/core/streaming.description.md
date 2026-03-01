# streaming

**File**: `src\infrastructure\tensorizer\core\streaming.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 80  
**Complexity**: 9 (moderate)

## Overview

Streaming reader for large models.

## Classes (1)

### `StreamingTensorizerReader`

Streaming reader for large models.

Loads tensors on-demand without loading entire file.

**Methods** (9):
- `__init__(self, path, config)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`
- `set_cache_limit(self, limit_bytes)`
- `get(self, name)`
- `_add_to_cache(self, name, tensor)`
- `preload(self, names)`
- `clear_cache(self)`
- `tensor_names(self)`

## Dependencies

**Imports** (8):
- `config.TensorizerConfig`
- `numpy`
- `pathlib.Path`
- `reader.TensorizerReader`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
