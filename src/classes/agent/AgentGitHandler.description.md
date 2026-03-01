# AgentGitHandler

**File**: `src\classes\agent\AgentGitHandler.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 84  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for AgentGitHandler.

## Classes (1)

### `AgentGitHandler`

Handles git operations for the Agent.

**Methods** (4):
- `__init__(self, repo_root, no_git, recorder)`
- `_record(self, action, result, meta)`
- `commit_changes(self, message, files)`
- `create_branch(self, branch_name)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `subprocess`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
