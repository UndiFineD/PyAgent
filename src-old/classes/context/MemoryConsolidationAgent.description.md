# MemoryConsolidationAgent

**File**: `src\classes\context\MemoryConsolidationAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 79  
**Complexity**: 4 (simple)

## Overview

Agent specializing in consolidating episodic memories into global project context.

## Classes (1)

### `MemoryConsolidationAgent`

**Inherits from**: BaseAgent

Refines project knowledge by analyzing past interactions and outcomes.

**Methods** (4):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `consolidate_all(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (12):
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.base_agent.utilities.create_main_function`
- `src.classes.context.GlobalContextEngine.GlobalContextEngine`
- `src.classes.context.MemoryEngine.MemoryEngine`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
