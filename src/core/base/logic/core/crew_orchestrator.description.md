# crew_orchestrator

**File**: `src\core\base\logic\core\crew_orchestrator.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 12 imports  
**Lines**: 386  
**Complexity**: 7 (moderate)

## Overview

CrewAI-style Multi-Agent Orchestration System

Inspired by CrewAI patterns from .external/action repository.
Implements role-based agent coordination with task dependencies and context sharing.

## Classes (7)

### `AgentRole`

**Inherits from**: Enum

Agent roles in the crew orchestration

### `TaskStatus`

**Inherits from**: Enum

Task execution status

### `AgentConfig`

Configuration for a crew agent

### `TaskConfig`

Configuration for a crew task

### `TaskResult`

Result of a task execution

### `CrewAgent`

A CrewAI-style agent with role-based capabilities.

Based on patterns from .external/action repository.

**Methods** (2):
- `__init__(self, config, llm_provider)`
- `_build_task_prompt(self, task, context)`

### `CrewOrchestrator`

Orchestrates multi-agent task execution with dependencies.

Inspired by CrewAI task coordination patterns.

**Methods** (5):
- `__init__(self)`
- `add_agent(self, agent)`
- `add_task(self, task)`
- `_get_executable_tasks(self, pending_tasks, completed_tasks)`
- `get_crew_status(self)`

## Dependencies

**Imports** (12):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `logging`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
