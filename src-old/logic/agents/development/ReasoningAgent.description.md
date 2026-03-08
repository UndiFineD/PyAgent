# ReasoningAgent

**File**: `src\logic\agents\development\ReasoningAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 99  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in logical reasoning, chain-of-thought analysis, and problem decomposition.

## Classes (1)

### `ReasoningAgent`

**Inherits from**: BaseAgent

Analyzes complex problems and provides a logical blueprint before action.

**Methods** (5):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `analyze(self, problem, context)`
- `analyze_tot(self, problem)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (7):
- `logging`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
