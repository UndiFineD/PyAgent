# ExecCommandMixin

**File**: `src\logic\agents\swarm\mixins\ExecCommandMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 89  
**Complexity**: 5 (moderate)

## Overview

Command and git execution logic for OrchestratorAgent.

## Classes (1)

### `ExecCommandMixin`

Mixin for fundamental command execution and git operations.

**Methods** (5):
- `_run_command(self, cmd, timeout, max_retries)`
- `_with_agent_env(self, agent_name)`
- `run_stats_update(self, files)`
- `run_tests(self, code_file)`
- `_commit_and_push(self, code_file)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `contextlib.contextmanager`
- `logging`
- `pathlib.Path`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
