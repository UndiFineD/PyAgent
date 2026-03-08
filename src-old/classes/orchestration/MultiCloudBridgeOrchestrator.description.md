# MultiCloudBridgeOrchestrator

**File**: `src\classes\orchestration\MultiCloudBridgeOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 69  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for MultiCloudBridgeOrchestrator.

## Classes (1)

### `MultiCloudBridgeOrchestrator`

Multi-Cloud Bridge Orchestrator: Manages agent communication and state 
synchronization across AWS, Azure, and GCP simulated environments.

**Methods** (5):
- `__init__(self, fleet_manager)`
- `register_cloud_node(self, node_id, provider, region)`
- `sync_state_cross_cloud(self, state_data, source_provider)`
- `get_bridge_topology(self)`
- `route_message(self, message, target_provider)`

## Dependencies

**Imports** (3):
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
