# environment_manager

**File**: `src\core\base\environment\environment_manager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 22 imports  
**Lines**: 324  
**Complexity**: 2 (simple)

## Overview

Module: environment_manager
Provides environment management for PyAgent multi-agent architecture.
Inspired by AEnvironment patterns for isolation and resource management.

## Classes (1)

### `EnvironmentManager`

Manages agent environments with isolation, resource limits, and lifecycle management.
Inspired by AEnvironment's containerized environment approach.

**Methods** (2):
- `__init__(self, base_dir)`
- `_start_cleanup_task(self)`

## Dependencies

**Imports** (22):
- `__future__.annotations`
- `asyncio`
- `contextlib.asynccontextmanager`
- `dataclasses.asdict`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `shutil`
- `src.core.base.common.models.base_models.EnvironmentConfig`
- `src.core.base.common.models.base_models.EnvironmentInstance`
- `src.core.base.common.models.core_enums.EnvironmentIsolation`
- `src.core.base.common.models.core_enums.EnvironmentStatus`
- `src.core.base.lifecycle.version.VERSION`
- `tempfile`
- ... and 7 more

---
*Auto-generated documentation*
