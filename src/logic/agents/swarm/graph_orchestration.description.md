# graph_orchestration

**File**: `src\logic\agents\swarm\graph_orchestration.py`  
**Type**: Python Module  
**Summary**: 14 classes, 0 functions, 19 imports  
**Lines**: 582  
**Complexity**: 32 (complex)

## Overview

Graph-based agent orchestration system inspired by LLM Tornado.

This module implements a sophisticated orchestration framework with:
- Orchestrator (graph): Manages the overall workflow
- Runner (node): Executes individual agent tasks
- Advancer (edge): Handles transitions between runners

Based on patterns from LLM Tornado's orchestration system.

## Classes (14)

### `ExecutionContext`

Simple execution context for orchestration.

**Methods** (2):
- `create_root(cls, context_id)`
- `create_child(self, child_id)`

### `OrchestrationStatus`

**Inherits from**: Enum

Status of orchestration execution.

### `OrchestrationState`

Base state for orchestration workflows.

**Methods** (1):
- `update_timestamp(self)`

### `GraphEdge`

Represents an edge between runners in the orchestration graph.

### `OrchestrationResult`

Result of a runner execution.

### `OrchestrationRunnable`

**Inherits from**: ABC

Abstract base class for orchestration runners (nodes).

**Methods** (3):
- `__init__(self, name, description)`
- `can_transition(self, result)`
- `__str__(self)`

### `OrchestrationAdvancer`

Handles transitions between runners based on execution results.

Inspired by LLM Tornado's advancer concept.

**Methods** (2):
- `__init__(self, edges)`
- `get_next_runners(self, current_runner, result)`

### `OrchestrationGraph`

**Inherits from**: Unknown

Immutable orchestration graph definition.

Based on LLM Tornado's OrchestrationGraph pattern.

**Methods** (5):
- `__init__(self, runnables, edges, entry_runnable, exit_runnables, initial_state)`
- `_create_default_state(self)`
- `get_runnable(self, name)`
- `get_next_runners(self, current_runner, result)`
- `is_exit_runnable(self, runnable)`

### `OrchestrationGraphBuilder`

**Inherits from**: Unknown

Fluent builder for creating orchestration graphs.

Inspired by LLM Tornado's OrchestrationGraphBuilder pattern.

**Methods** (7):
- `__init__(self)`
- `with_initial_state(self, state)`
- `add_runnable(self, runnable)`
- `set_entry_runnable(self, runnable)`
- `set_exit_runnable(self, runnable, allow_dead_end)`
- `add_edge(self, source, target, condition)`
- `build(self)`

### `Orchestrator`

**Inherits from**: Unknown

Main orchestrator that executes orchestration graphs.

Based on LLM Tornado's orchestrator concept.

**Methods** (4):
- `__init__(self, graph)`
- `cancel(self)`
- `is_running(self)`
- `is_cancelled(self)`

### `AgentTaskState`

**Inherits from**: OrchestrationState

State for agent task orchestration.

### `AgentRunner`

**Inherits from**: OrchestrationRunnable

Runner that executes agent tasks.

**Methods** (1):
- `__init__(self, name, agent_function)`

### `ConditionalRunner`

**Inherits from**: OrchestrationRunnable

Runner that executes based on conditions.

**Methods** (1):
- `__init__(self, name, condition_func, true_runner, false_runner)`

### `GraphOrchestrationMixin`

Mixin to add graph-based orchestration capabilities to PyAgent orchestrators.

This provides the LLM Tornado-inspired orchestration framework.

**Methods** (6):
- `__init__(self)`
- `create_orchestration_builder(self)`
- `create_agent_task_builder(self)`
- `register_orchestrator(self, name, orchestrator)`
- `get_orchestrator(self, name)`
- `list_orchestrators(self)`

## Dependencies

**Imports** (19):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `logging`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Generic`
- `typing.List`
- `typing.Optional`
- ... and 4 more

---
*Auto-generated documentation*
