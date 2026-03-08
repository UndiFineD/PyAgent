# ContextVersioningMixin

**File**: `src\logic\agents\cognitive\ContextVersioningMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 96  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for ContextVersioningMixin.

## Classes (1)

### `ContextVersioningMixin`

Versioning and compression methods for ContextAgent.

**Methods** (7):
- `create_version(self, version, changes, author)`
- `get_versions(self)`
- `get_latest_version(self)`
- `get_version_diff(self, v1, v2)`
- `compress_content(self, content)`
- `decompress_content(self, compressed)`
- `get_compression_ratio(self, content)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `datetime.datetime`
- `hashlib`
- `logging`
- `src.logic.agents.cognitive.context.models.ContextVersion.ContextVersion`
- `typing.Any`
- `zlib`

---
*Auto-generated documentation*
