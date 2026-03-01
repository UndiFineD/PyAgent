# multi_agent_orchestrator

**File**: `src\core\base\logic\multi_agent_orchestrator.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 17 imports  
**Lines**: 435  
**Complexity**: 13 (moderate)

## Overview

Multi-Agent Orchestrator Core - Unified Agent Management System
=================================================================

Inspired by big-3-super-agent's orchestration patterns, this core provides:
- Unified interface for managing multiple agent types (voice, coding, browser)
- Agent registry with persistent session management
- Tool-based dispatch system for agent orchestration
- Background task processing with status tracking
- Working directory management per agent type

Key Patterns Extracted from big-3-super-agent:
- Agent registry system with session persistence
- Tool-based orchestration via function calls
- Background processing with operator logs
- Multi-agent coordination and lifecycle management

## Classes (3)

### `AgentMetadata`

Metadata for registered agents.

### `TaskResult`

Result of an agent task execution.

### `MultiAgentOrchestratorCore`

Unified orchestrator for managing multiple agent types.

Provides a centralized system for:
- Agent registration and lifecycle management
- Task dispatch and execution tracking
- Working directory management
- Tool-based orchestration interface

**Methods** (13):
- `__init__(self, base_working_dir)`
- `_load_registry(self)`
- `_save_registry(self)`
- `register_agent_type(self, agent_type, handler)`
- `create_agent(self, agent_type, agent_name, capabilities, context)`
- `dispatch_task(self, agent_name, task_description, parameters, context)`
- `get_task_status(self, task_id)`
- `list_agents(self, agent_type)`
- `delete_agent(self, agent_name)`
- `get_agent_tools(self, agent_name)`
- ... and 3 more methods

## Dependencies

**Imports** (17):
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timezone`
- `json`
- `pathlib.Path`
- `shutil`
- `src.core.base.common.models.communication_models.CascadeContext`
- `src.core.base.state.agent_state_manager.StateTransaction`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- ... and 2 more

---
*Auto-generated documentation*
