# ResultCache

**File**: `src\core\base\utils\ResultCache.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 123  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `ResultCache`

Cache agent results for reuse.

Example:
    cache=ResultCache()

    # Check cache
    result=cache.get("test.py", "coder", content_hash)
    if result is None:
        result=run_coder("test.py")
        cache.set("test.py", "coder", content_hash, result)

**Methods** (6):
- `__init__(self, cache_dir)`
- `_make_key(self, file_path, agent_name, content_hash)`
- `get(self, file_path, agent_name, content_hash)`
- `set(self, file_path, agent_name, content_hash, result, ttl_seconds)`
- `invalidate(self, file_path)`
- `clear(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `pathlib.Path`
- `src.core.base.models.CachedResult`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
