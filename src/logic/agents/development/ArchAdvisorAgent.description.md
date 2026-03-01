# ArchAdvisorAgent

**File**: `src\logic\agents\development\ArchAdvisorAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 75  
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

**Imports** (6):
- `__future__.annotations`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.engines.GraphContextEngine.GraphContextEngine`
- `src.logic.agents.development.ArchCore.ArchCore`

---
*Auto-generated documentation*
