# artifact_cleanup_core

**File**: `src\core\base\logic\core\artifact_cleanup_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 106  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for artifact_cleanup_core.

## Classes (1)

### `ArtifactCleanupCore`

Background worker for disk maintenance of modality artifacts (images/test logs).
Pattern harvested from 4o-ghibli-at-home.

**Methods** (2):
- `__init__(self, base_dir, interval, ttl, patterns)`
- `force_purge(self)`

## Dependencies

**Imports** (8):
- `asyncio`
- `logging`
- `os`
- `pathlib.Path`
- `time`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
