# delegation

**File**: `src\core\base\delegation.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 101  
**Complexity**: 1 (simple)

## Overview

Delegation management for agent cascading.
Enables agents to launch sub-tasks by spawning other specialized agents.

## Classes (1)

### `AgentDelegator`

Handles cascading sub-tasks to other agents.

**Methods** (1):
- `delegate(agent_type, prompt, current_agent_name, current_file_path, current_model, target_file, context, priority)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `importlib`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.models.AgentPriority`
- `src.core.base.models.CascadeContext`
- `src.core.base.registry.AgentRegistry`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
