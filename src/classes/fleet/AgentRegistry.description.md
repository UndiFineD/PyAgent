# AgentRegistry

**File**: `src\classes\fleet\AgentRegistry.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 16 imports  
**Lines**: 351  
**Complexity**: 21 (complex)

## Overview

Registry for mapping agent names to their implementations and initialization logic.

## Classes (2)

### `LazyAgentMap`

**Inherits from**: dict

A dictionary that instantiates agents only when they are first accessed.

**Methods** (20):
- `__init__(self, workspace_root, registry_configs, fleet_instance)`
- `_scan_workspace_for_agents(self)`
- `_load_manifests(self)`
- `try_reload(self, key)`
- `check_for_registry_cycles(self)`
- `__contains__(self, key)`
- `keys(self)`
- `__iter__(self)`
- `__len__(self)`
- `items(self)`
- ... and 10 more methods

### `AgentRegistry`

Registry for mapping agent names to their implementations via lazy loading.

**Methods** (1):
- `get_agent_map(workspace_root, fleet_instance)`

## Dependencies

**Imports** (16):
- `AgentRegistryCore.AgentRegistryCore`
- `BootstrapConfigs.BOOTSTRAP_AGENTS`
- `FleetManager.FleetManager`
- `ResilientStubs.ResilientStub`
- `__future__.annotations`
- `collections.abc.Iterable`
- `importlib`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.Version.SDK_VERSION`
- `src.core.base.Version.VERSION`
- `src.logic.agents.system.MCPAgent.MCPAgent`
- `typing.Any`
- ... and 1 more

---
*Auto-generated documentation*
