# pyagent_cli

**File**: `src\pyagent_cli.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 11 imports  
**Lines**: 161  
**Complexity**: 4 (simple)

## Overview

PyAgent CLI Interface.
Connects to the Fleet Load Balancer via the Agent API Server.

## Functions (4)

### `check_server()`

Verify that the API server is running with 15m TTL caching.

### `list_agents()`

Get list of active agents from the fleet.

### `run_task(agent_id, task)`

Dispatch a task to a specific agent via the Load Balancer.

### `main()`

## Dependencies

**Imports** (11):
- `argparse`
- `json`
- `pathlib.Path`
- `requests`
- `rich.console.Console`
- `rich.panel.Panel`
- `rich.table.Table`
- `src.classes.backend.LocalContextRecorder.LocalContextRecorder`
- `src.classes.base_agent.ConnectivityManager.ConnectivityManager`
- `src.version.VERSION`
- `sys`

---
*Auto-generated documentation*
