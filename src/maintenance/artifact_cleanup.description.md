# artifact_cleanup

**File**: `src\maintenance\artifact_cleanup.py`  
**Type**: Python Module  
**Summary**: 1 classes, 1 functions, 8 imports  
**Lines**: 223  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for artifact_cleanup.

## Classes (1)

### `ArtifactCleanupCore`

Core for managing artifact cleanup in PyAgent.

Implements secondary cleanup workers that periodically purge generated artifacts
(images, logs, temporary files) from disk based on TTL (Time To Live).

Inspired by 4o-ghibli-at-home's background cleanup patterns.

**Methods** (4):
- `__init__(self, cleanup_interval, default_ttl, max_age_overrides, cleanup_dirs, dry_run)`
- `_should_cleanup_file(self, file_path, current_time)`
- `_get_ttl_for_file(self, file_path)`
- `get_stats(self)`

## Functions (1)

### `get_artifact_cleanup_core()`

Get the global artifact cleanup core instance.

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
