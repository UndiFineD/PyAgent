# SelfOptimizerAgent

**File**: `src\classes\coder\SelfOptimizerAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 97  
**Complexity**: 4 (simple)

## Overview

Agent specializing in self-optimization and roadmap refinement.

## Classes (1)

### `SelfOptimizerAgent`

**Inherits from**: BaseAgent

Analyses the workspace status and suggests strategic improvements.

**Methods** (4):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `analyze_roadmap(self, improvements_path)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (11):
- `logging`
- `os`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `src.classes.stats.ObservabilityEngine.ObservabilityEngine`
- `src.classes.stats.ResourceMonitor.ResourceMonitor`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
