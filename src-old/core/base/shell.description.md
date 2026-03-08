# shell

**File**: `src\core\base\shell.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 13 imports  
**Lines**: 175  
**Complexity**: 2 (simple)

## Overview

Shell execution core for agents.
Handles subprocess spawning, environment propagation, and interaction recording.

## Classes (2)

### `EnvironmentSanitizer`

Filters environment variables to prevent secret leakage (Phase 266).

**Methods** (1):
- `sanitize(cls, env)`

### `ShellExecutor`

Safely executes shell commands and records outcomes.

**Methods** (1):
- `run_command(cmd, workspace_root, agent_name, models_config, recorder, timeout, max_retries)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `asyncio`
- `json`
- `logging`
- `os`
- `src.core.base.sandbox.SandboxManager`
- `src.core.base.version.VERSION`
- `subprocess`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
