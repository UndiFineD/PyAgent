# OllamaConnectorAgent

**File**: `src\logic\agents\infrastructure\OllamaConnectorAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 84  
**Complexity**: 3 (simple)

## Overview

Agent for connecting to local Ollama instances on edge nodes (Phase 125).

## Classes (1)

### `OllamaConnectorAgent`

**Inherits from**: BaseAgent

Handles local inference requests via the Ollama API.

**Methods** (3):
- `__init__(self, file_path, endpoint)`
- `check_availability(self)`
- `generate_local(self, prompt, model)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `requests`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
