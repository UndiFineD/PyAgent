# OrchestratorRegistry

**File**: `src\classes\fleet\OrchestratorRegistry.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 14 imports  
**Lines**: 143  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for OrchestratorRegistry.

## Classes (2)

### `LazyOrchestratorMap`

A dictionary-like object that instantiates orchestrators only when accessed.

**Methods** (7):
- `__init__(self, fleet_instance)`
- `_scan_workspace_for_orchestrators(self)`
- `_load_manifests(self)`
- `__getattr__(self, name)`
- `_instantiate(self, key, config)`
- `keys(self)`
- `__contains__(self, key)`

### `OrchestratorRegistry`

Class OrchestratorRegistry implementation.

**Methods** (1):
- `get_orchestrator_map(fleet_instance)`

## Dependencies

**Imports** (14):
- `BootstrapConfigs.BOOTSTRAP_ORCHESTRATORS`
- `OrchestratorRegistryCore.OrchestratorRegistryCore`
- `ResilientStubs.ResilientStub`
- `importlib`
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
