# LintingAgent

**File**: `src\logic\agents\development\LintingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 91  
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

**Imports** (5):
- `__future__.annotations`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `subprocess`

---
*Auto-generated documentation*
