# OrchestratorPluginMixin

**File**: `src\logic\agents\swarm\OrchestratorPluginMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 112  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for OrchestratorPluginMixin.

## Classes (1)

### `OrchestratorPluginMixin`

Plugin system methods for OrchestratorAgent.

**Methods** (5):
- `register_plugin(self, plugin)`
- `unregister_plugin(self, plugin_name)`
- `get_plugin(self, plugin_name)`
- `run_plugins(self, file_path)`
- `load_plugins_from_config(self, plugin_configs)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `concurrent.futures.ThreadPoolExecutor`
- `concurrent.futures.TimeoutError`
- `importlib.util`
- `logging`
- `pathlib.Path`
- `src.core.base.AgentPluginBase.AgentPluginBase`
- `src.core.base.models.AgentPluginConfig`
- `typing.Any`

---
*Auto-generated documentation*
