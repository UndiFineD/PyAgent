# IdiomExtractorAgent

**File**: `src\classes\specialized\IdiomExtractorAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 104  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for IdiomExtractorAgent.

## Classes (1)

### `IdiomExtractorAgent`

**Inherits from**: BaseAgent

Agent responsible for extracting project-specific coding idioms and patterns.
Maintains a .pyagent_idioms.json file to guide future code generation.

**Methods** (3):
- `__init__(self, file_path)`
- `extract_idioms(self, directory)`
- `get_current_idioms(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `json`
- `logging`
- `os`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
