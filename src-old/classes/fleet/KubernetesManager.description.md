# KubernetesManager

**File**: `src\classes\fleet\KubernetesManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 60  
**Complexity**: 4 (simple)

## Overview

Manager for scaling agents via Kubernetes pods.
Handles deployment and lifecycle of agent-specific containers.

## Classes (1)

### `KubernetesManager`

Orchestrates agent execution within a K8s cluster.

**Methods** (4):
- `__init__(self, namespace)`
- `deploy_agent_pod(self, agent_name, image)`
- `scale_deployment(self, deployment_name, replicas)`
- `get_cluster_status(self)`

## Dependencies

**Imports** (6):
- `json`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
