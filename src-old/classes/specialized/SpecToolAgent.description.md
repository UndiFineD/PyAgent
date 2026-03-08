# SpecToolAgent

**File**: `src\classes\specialized\SpecToolAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 168  
**Complexity**: 8 (moderate)

## Overview

Agent specializing in generating tools and code from specifications (OpenAPI, JSON Schema, MCP).

## Classes (1)

### `SpecToolAgent`

**Inherits from**: BaseAgent

Generates Python tool wrappers from specifications and manages OpenSpec SDD workflows.

**Methods** (8):
- `__init__(self, file_path)`
- `generate_sdd_spec(self, feature_name, details)`
- `confirm_proceed(self, confirmation)`
- `init_openspec(self)`
- `create_proposal(self, name, intent)`
- `archive_change(self, name)`
- `generate_tool_from_spec(self, spec_path)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.Optional`

---
*Auto-generated documentation*
