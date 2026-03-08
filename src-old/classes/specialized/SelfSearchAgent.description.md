# SelfSearchAgent

**File**: `src\classes\specialized\SelfSearchAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 71  
**Complexity**: 4 (simple)

## Overview

Agent specializing in Self-Search Reinforcement Learning (SSRL) patterns.

## Classes (1)

### `SelfSearchAgent`

**Inherits from**: BaseAgent

Provides internal knowledge retrieval using structural prompting (SSRL pattern).

**Methods** (4):
- `__init__(self, file_path)`
- `generate_search_structure(self, query)`
- `perform_internal_search(self, query)`
- `improve_content(self, query)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
