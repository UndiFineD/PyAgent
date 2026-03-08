# LintingAgent

**File**: `src\classes\coder\LintingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 79  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in code quality, linting, and style enforcement.

## Classes (1)

### `LintingAgent`

**Inherits from**: BaseAgent

Ensures code adheres to quality standards by running linters.

**Methods** (5):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `run_flake8(self, target_path)`
- `run_mypy(self, target_path)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (9):
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `subprocess`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
