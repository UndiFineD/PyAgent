# FleetManager

**File**: `src\classes\fleet\FleetManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 29 imports  
**Lines**: 559  
**Complexity**: 24 (complex)

## Overview

Coordinator for deploying and aggregating results from multiple agents.

## Classes (1)

### `FleetManager`

The central hub for the PyAgent ecosystem. Orchestrates a swarm of specialized
agents to complete complex workflows, manages resource scaling, and ensures
system-wide stability through various orchestrators.

**Methods** (24):
- `__getattr__(self, name)`
- `__init__(self, workspace_root)`
- `telemetry(self)`
- `registry(self)`
- `signals(self)`
- `recorder(self)`
- `sql_metadata(self)`
- `self_healing(self)`
- `self_improvement(self)`
- `global_context(self)`
- ... and 14 more methods

## Dependencies

**Imports** (29):
- `concurrent.futures.ThreadPoolExecutor`
- `concurrent.futures.TimeoutError`
- `datetime.datetime`
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.backend.LocalContextRecorder.LocalContextRecorder`
- `src.classes.backend.SqlAgent.SqlAgent`
- `src.classes.base_agent.BaseAgent`
- `src.classes.context.GlobalContextEngine.GlobalContextEngine`
- `src.classes.fleet.AgentRegistry.AgentRegistry`
- `src.classes.fleet.OrchestratorRegistry.OrchestratorRegistry`
- `src.classes.fleet.VersionGate.VersionGate`
- `src.classes.fleet.WorkflowState.WorkflowState`
- `src.classes.orchestration.SelfHealingOrchestrator.SelfHealingOrchestrator`
- ... and 14 more

---
*Auto-generated documentation*
