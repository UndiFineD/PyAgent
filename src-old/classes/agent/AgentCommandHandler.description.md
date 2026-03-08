# AgentCommandHandler

**File**: `src\classes\agent\AgentCommandHandler.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 15 imports  
**Lines**: 171  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for AgentCommandHandler.

## Classes (1)

### `AgentCommandHandler`

Handles command execution for the Agent, including sub-agent orchestration.

**Methods** (6):
- `__init__(self, repo_root, models_config, recorder)`
- `_record(self, action, result, meta)`
- `run_command(self, cmd, timeout, max_retries)`
- `_prepare_command_environment(self, cmd)`
- `_get_agent_env_vars(self, agent_name)`
- `with_agent_env(self, agent_name)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `collections.abc.Iterator`
- `contextlib`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `subprocess`
- `sys`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
