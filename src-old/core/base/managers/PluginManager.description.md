# PluginManager

**File**: `src\core\base\managers\PluginManager.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 12 imports  
**Lines**: 271  
**Complexity**: 10 (moderate)

## Overview

Python module containing implementation for PluginManager.

## Classes (2)

### `PluginMetadata`

Strictly typed metadata for a plugin.

**Methods** (1):
- `get(self, key, default)`

### `PluginManager`

Modernized PluginManager (Phase 226).
Handles discovery, manifest enforcement, health tracking, and graceful shutdown.

**Methods** (9):
- `__init__(self, workspace_root)`
- `discover(self)`
- `validate_version(self, required_version)`
- `load_plugin(self, plugin_name)`
- `_load_sandboxed_plugin(self, name, meta)`
- `_setup_permission_proxy(self, name, meta)`
- `shutdown_all(self)`
- `activate_all(self)`
- `deactivate(self, name)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `dataclasses.dataclass`
- `docker`
- `importlib`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.AgentPluginBase.AgentPluginBase`
- `src.core.base.Version.SDK_VERSION`
- `src.infrastructure.fleet.VersionGate.VersionGate`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
