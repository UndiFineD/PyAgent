# agent_models

**File**: `src\core\base\models\agent_models.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 14 imports  
**Lines**: 127  
**Complexity**: 7 (moderate)

## Overview

Models for agent configuration, state, and plugins.

## Classes (8)

### `AgentConfig`

Agent configuration from environment or file.

### `ComposedAgent`

Configuration for agent composition.

### `AgentHealthCheck`

Health check result for an agent.

### `AgentPluginConfig`

Configuration for an agent plugin.

### `ExecutionProfile`

A profile for agent execution settings.

### `AgentPipeline`

Chains agent steps sequentially.

**Methods** (2):
- `add_step(self, name, func)`
- `execute(self, data)`

### `AgentParallel`

Executes agent branches in parallel conceptually.

**Methods** (2):
- `add_branch(self, name, func)`
- `execute(self, data)`

### `AgentRouter`

Routes input based on conditions.

**Methods** (3):
- `add_route(self, condition, handler)`
- `set_default(self, handler)`
- `route(self, data)`

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `base_models._empty_dict_str_any`
- `base_models._empty_dict_str_callable_any_any`
- `base_models._empty_list_str`
- `collections.abc.Callable`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enums.AgentPriority`
- `enums.HealthStatus`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
