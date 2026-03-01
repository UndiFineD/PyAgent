# PluginManager

**File**: `src\classes\fleet\PluginManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 108  
**Complexity**: 4 (simple)

## Overview

Manager for loading 3rd party agent extensions dynamically.
Scans the 'plugins' directory for agent implementations.

## Classes (1)

### `PluginManager`

Modernized PluginManager.
Handles discovery, version gatekeeping, and lazy loading for community extensions.

**Methods** (4):
- `__init__(self, workspace_root)`
- `discover(self)`
- `validate_version(self, required_version)`
- `load_resource(self, plugin_name)`

## Dependencies

**Imports** (11):
- `VersionGate.VersionGate`
- `importlib.util`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.version.SDK_VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
