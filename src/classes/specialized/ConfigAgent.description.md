# ConfigAgent

**File**: `src\classes\specialized\ConfigAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 62  
**Complexity**: 4 (simple)

## Overview

Agent specializing in configuration validation, secrets checking, and environment setup.
Inspired by external-secrets and infrastructure-as-code patterns.

## Classes (1)

### `ConfigAgent`

**Inherits from**: BaseAgent

Ensures the agent fleet has all necessary configurations and API keys.

**Methods** (4):
- `__init__(self, file_path)`
- `validate_env(self)`
- `validate_models_yaml(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (10):
- `logging`
- `os`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `yaml`

---
*Auto-generated documentation*
