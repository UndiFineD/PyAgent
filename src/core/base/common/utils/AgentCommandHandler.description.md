# AgentCommandHandler

**File**: `src\core\base\common\utils\AgentCommandHandler.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 124  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for AgentCommandHandler.

## Classes (1)

### `AgentCommandHandler`

Handles command execution for the Agent, including sub-agent orchestration.

**Methods** (3):
- `__init__(self, repo_root, models_config)`
- `run_command(self, cmd, timeout, max_retries)`
- `with_agent_env(self, agent_name)`

## Dependencies

**Imports** (11):
- `contextlib`
- `logging`
- `os`
- `pathlib.Path`
- `subprocess`
- `sys`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
