# agent_pool_manager

**File**: `src\core\base\logic\agent_pool_manager.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 22 imports  
**Lines**: 387  
**Complexity**: 17 (moderate)

## Overview

Agent Pool Manager - Self-evolving agent pool with task-driven creation and evolution
Based on the Autonomous Orchestration Ecosystem from agent-orchestrator-self-evolving-subagent

## Classes (4)

### `AgentStatus`

**Inherits from**: Enum

Agent lifecycle status

### `AgentManifest`

Metadata and metrics for an agent

**Methods** (2):
- `to_dict(self)`
- `from_dict(cls, data)`

### `TaskRequirements`

Requirements analysis for a task

### `AgentPoolManager`

Self-evolving agent pool manager
Implements the Autonomous Orchestration Ecosystem pattern

**Methods** (15):
- `__init__(self, manifest_dir)`
- `_ensure_manifest_dir(self)`
- `register_agent(self, agent, capabilities)`
- `update_agent_metrics(self, agent_name, success, execution_time)`
- `analyze_task_requirements(self, task_description, context)`
- `find_optimal_agent(self, requirements)`
- `decide_agent_action(self, coverage_rate, requirements)`
- `create_integrated_agent(self, requirements, candidate_agents)`
- `create_specialized_agent(self, requirements)`
- `_calculate_coverage(self, requirements, manifest)`
- ... and 5 more methods

## Dependencies

**Imports** (22):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `glob`
- `json`
- `logging`
- `os`
- `src.core.base.common.models.communication_models.CascadeContext`
- `src.core.base.lifecycle.base_agent.BaseAgent`
- `statistics`
- `time`
- `typing.Any`
- ... and 7 more

---
*Auto-generated documentation*
