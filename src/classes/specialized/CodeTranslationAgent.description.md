# CodeTranslationAgent

**File**: `src\classes\specialized\CodeTranslationAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 73  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for CodeTranslationAgent.

## Classes (1)

### `CodeTranslationAgent`

**Inherits from**: BaseAgent

Handles translation of codebases between different programming languages.
Supports mapping logic, syntax transformations, and multi-file translation.

**Methods** (5):
- `__init__(self, workspace_path)`
- `translate_file(self, source_code, from_lang, to_lang)`
- `_mock_python_to_rust(self, code)`
- `_mock_python_to_js(self, code)`
- `get_translation_stats(self)`

## Dependencies

**Imports** (5):
- `os`
- `src.classes.base_agent.BaseAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
