# QualityGateAgent

**File**: `src\classes\coder\QualityGateAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 115  
**Complexity**: 6 (moderate)

## Overview

Agent specializing in automated quality gates and release validation.

## Classes (1)

### `QualityGateAgent`

**Inherits from**: BaseAgent

Enforces thresholds for code quality, test coverage, and security before deployment.

**Methods** (6):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `check_gates(self)`
- `validate_against_blueprint(self, result, blueprint)`
- `validate_release(self, current_result, reasoning_blueprint)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (12):
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.base_agent.utilities.create_main_function`
- `subprocess`
- `sys`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
