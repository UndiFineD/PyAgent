# DirectorAgent

**File**: `src\classes\orchestration\DirectorAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 220  
**Complexity**: 6 (moderate)

## Overview

Agent specializing in Project Management and Multi-Agent Orchestration.

## Classes (1)

### `DirectorAgent`

**Inherits from**: BaseAgent

Orchestrator agent that decomposes complex tasks and delegates to specialists.

**Methods** (6):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `_get_available_agents(self)`
- `_handle_agent_failure(self, event)`
- `_handle_agent_success(self, event)`
- `_update_improvement_status(self, title, status)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.create_main_function`
- `src.core.base.Version.VERSION`
- `src.infrastructure.orchestration.state.StatusManager.StatusManager`

---
*Auto-generated documentation*
