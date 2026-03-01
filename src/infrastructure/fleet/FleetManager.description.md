# FleetManager

**File**: `src\infrastructure\fleet\FleetManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 24 imports  
**Lines**: 192  
**Complexity**: 1 (simple)

## Overview

Coordinator for deploying and aggregating results from multiple agents.

## Classes (1)

### `FleetManager`

**Inherits from**: FleetTaskMixin, FleetRoutingMixin, FleetLifecycleMixin, FleetLookupMixin, FleetDiscoveryMixin, FleetDelegationMixin, FleetUpdateMixin

The central hub for the PyAgent ecosystem. Orchestrates a swarm of specialized
agents to complete complex workflows, manages resource scaling, and ensures
system-wide stability through various orchestrators.

**Methods** (1):
- `__init__(self, workspace_root)`

## Dependencies

**Imports** (24):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.Version.VERSION`
- `src.infrastructure.fleet.AgentRegistry.AgentRegistry`
- `src.infrastructure.fleet.FleetConsensusManager.FleetConsensusManager`
- `src.infrastructure.fleet.FleetExecutionCore.FleetExecutionCore`
- `src.infrastructure.fleet.FleetInteractionRecorder.FleetInteractionRecorder`
- `src.infrastructure.fleet.FleetLifecycleManager.FleetLifecycleManager`
- `src.infrastructure.fleet.FleetRoutingCore.FleetRoutingCore`
- `src.infrastructure.fleet.OrchestratorRegistry.OrchestratorRegistry`
- `src.infrastructure.fleet.WorkflowState.WorkflowState`
- `src.infrastructure.fleet.mixins.FleetDelegationMixin.FleetDelegationMixin`
- `src.infrastructure.fleet.mixins.FleetDiscoveryMixin.FleetDiscoveryMixin`
- `src.infrastructure.fleet.mixins.FleetLifecycleMixin.FleetLifecycleMixin`
- ... and 9 more

---
*Auto-generated documentation*
