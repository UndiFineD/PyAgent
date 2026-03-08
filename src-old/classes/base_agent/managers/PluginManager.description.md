# PluginManager

**File**: `src\classes\base_agent\managers\PluginManager.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 19 imports  
**Lines**: 169  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for PluginManager.

## Classes (2)

### `PluginMetadata`

Strictly typed metadata for a plugin.

### `PluginManager`

Modernized PluginManager (Phase 226).
Handles discovery, manifest enforcement, health tracking, and graceful shutdown.

**Methods** (7):
- `__init__(self, workspace_root)`
- `discover(self)`
- `validate_version(self, required_version)`
- `load_plugin(self, plugin_name)`
- `shutdown_all(self)`
- `activate_all(self)`
- `deactivate(self, name)`

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `importlib`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.AgentPluginBase.AgentPluginBase`
- `src.core.base.version.SDK_VERSION`
- `src.core.base.version.VERSION`
- `src.infrastructure.fleet.VersionGate.VersionGate`
- `sys`
- `typing.Any`
- `typing.Dict`
- ... and 4 more

---
*Auto-generated documentation*
