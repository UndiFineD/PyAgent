# AgentPluginBase

**File**: `src\classes\agent\AgentPluginBase.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 89  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `AgentPluginBase`

**Inherits from**: ABC

Abstract base class for agent plugins.

Provides interface for third - party agents to integrate with
the agent orchestrator without modifying core code.

Attributes:
    name: Plugin name.
    priority: Execution priority.
    config: Plugin configuration.

**Methods** (6):
- `__init__(self, name, priority, config)`
- `run(self, file_path, context)`
- `setup(self)`
- `shutdown(self)`
- `teardown(self)`
- `health_check(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `logging`
- `pathlib.Path`
- `src.core.base.models.AgentHealthCheck`
- `src.core.base.models.AgentPriority`
- `src.core.base.models.HealthStatus`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
