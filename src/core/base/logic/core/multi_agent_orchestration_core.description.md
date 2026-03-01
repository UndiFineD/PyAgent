# multi_agent_orchestration_core

**File**: `src\core\base\logic\core\multi_agent_orchestration_core.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 17 imports  
**Lines**: 193  
**Complexity**: 2 (simple)

## Overview

Multi-Agent Orchestration Core
Implements structured multi-agent coordination patterns inspired by CrewAI and OpenAI Agents SDK.
Provides deterministic agent interactions with Pydantic-based structured outputs.

## Classes (5)

### `AgentTask`

**Inherits from**: BaseModel

Represents a task to be executed by an agent.

### `AgentResult`

**Inherits from**: BaseModel

Standardized result format from agent execution.

### `OrchestrationPlan`

**Inherits from**: BaseModel

Plan for multi-agent task execution.

### `AgentCoordinator`

**Inherits from**: ABC

Abstract base class for agent coordinators.

### `MultiAgentOrchestrationCore`

**Inherits from**: BaseCore

Core for coordinating multiple agents in structured workflows.
Inspired by CrewAI patterns and OpenAI Agents SDK structured outputs.

**Methods** (2):
- `__init__(self, coordinator)`
- `get_task_results(self)`

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `logging`
- `pydantic.BaseModel`
- `pydantic.Field`
- `src.core.base.common.base_core.BaseCore`
- `src.core.base.common.models.communication_models.CascadeContext`
- `typing.Any`
- `typing.AsyncGenerator`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 2 more

---
*Auto-generated documentation*
