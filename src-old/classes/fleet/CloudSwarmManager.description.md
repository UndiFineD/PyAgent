# CloudSwarmManager

**File**: `src\classes\fleet\CloudSwarmManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 97  
**Complexity**: 5 (moderate)

## Overview

Manager for cross-cloud swarm orchestration.
Handles resource provisioning and agent deployment across AWS, Azure, and GCP.

## Classes (1)

### `CloudSwarmManager`

Orchestrates resources and deployments across multiple cloud providers.

**Methods** (5):
- `__init__(self, config_path)`
- `provision_resource(self, provider, resource_type, specs)`
- `deploy_agent_to_cloud(self, agent_name, resource_id)`
- `list_cloud_resources(self)`
- `terminate_cloud_resource(self, resource_id)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
