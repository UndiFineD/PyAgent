# ArchAdvisorAgent

**File**: `src\classes\coder\ArchAdvisorAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 65  
**Complexity**: 4 (simple)

## Overview

Agent specializing in architectural analysis and decoupled system design.

## Classes (1)

### `ArchAdvisorAgent`

**Inherits from**: BaseAgent

Analyzes codebase coupling and suggests architectural refactors.

**Methods** (4):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `analyze_coupling(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (10):
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `src.classes.context.GraphContextEngine.GraphContextEngine`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
