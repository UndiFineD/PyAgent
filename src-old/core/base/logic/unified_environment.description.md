# unified_environment

**File**: `src\core\base\logic\unified_environment.py`  
**Type**: Python Module  
**Summary**: 9 classes, 0 functions, 16 imports  
**Lines**: 428  
**Complexity**: 24 (complex)

## Overview

Unified Environment Abstraction - AEnvironment-inspired "Everything as Environment"
Based on AEnvironment's philosophy of abstracting tools, agents, and environments uniformly

## Classes (9)

### `EnvironmentStatus`

**Inherits from**: Enum

Environment lifecycle status

### `EnvironmentResult`

Result from environment execution

### `EnvironmentCapabilities`

Capabilities exposed by an environment

### `EnvironmentProtocol`

**Inherits from**: Protocol

Protocol for environment-like objects

**Methods** (3):
- `name(self)`
- `status(self)`
- `get_capabilities(self)`

### `BaseEnvironment`

**Inherits from**: ABC

Abstract base class for all environments
Everything can be treated as an environment: tools, agents, benchmarks, etc.

**Methods** (7):
- `__init__(self, name, config)`
- `status(self)`
- `uptime(self)`
- `execution_count(self)`
- `get_capabilities(self)`
- `_update_status(self, status)`
- `_record_execution(self)`

### `ToolEnvironment`

**Inherits from**: BaseEnvironment

Environment that wraps a tool/function
Treats individual tools as environments

**Methods** (2):
- `__init__(self, name, tool_func, config)`
- `get_capabilities(self)`

### `AgentEnvironment`

**Inherits from**: BaseEnvironment

Environment that wraps an agent
Treats agents as environments that can be called like tools

**Methods** (2):
- `__init__(self, name, agent_instance, config)`
- `get_capabilities(self)`

### `CompositeEnvironment`

**Inherits from**: BaseEnvironment

Environment that composes multiple sub-environments
Enables complex multi-environment orchestration

**Methods** (4):
- `__init__(self, name, sub_environments, config)`
- `_aggregate_capabilities(self)`
- `_route_action(self, action, parameters)`
- `get_capabilities(self)`

### `EnvironmentRegistry`

Registry for managing environments
Provides unified access to all environment types

**Methods** (6):
- `__init__(self)`
- `register_environment_type(self, env_type, env_class)`
- `create_environment(self, env_type, name)`
- `get_environment(self, name)`
- `list_environments(self)`
- `get_environment_status(self)`

## Dependencies

**Imports** (16):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `json`
- `logging`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Protocol`
- ... and 1 more

---
*Auto-generated documentation*
