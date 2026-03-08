# skill_manager_core

**File**: `src\core\base\logic\core\skill_manager_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 100  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for skill_manager_core.

## Classes (1)

### `SkillManagerCore`

Manages the dynamic discovery and registration of agent skills (MCP tools).
Harvested from awesome-mcp patterns.

**Methods** (2):
- `__init__(self, skills_dir)`
- `get_skill_manifest(self, skill_name)`

## Dependencies

**Imports** (10):
- `asyncio`
- `json`
- `os`
- `shutil`
- `src.core.base.agent_state_manager.StateTransaction`
- `subprocess`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
