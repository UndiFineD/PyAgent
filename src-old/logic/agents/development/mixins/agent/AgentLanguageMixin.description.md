# AgentLanguageMixin

**File**: `src\logic\agents\development\mixins\agent\AgentLanguageMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 61  
**Complexity**: 6 (moderate)

## Overview

Language detection and validation logic for CoderAgent.

## Classes (1)

### `AgentLanguageMixin`

Mixin for code language detection and syntax validation.

**Methods** (6):
- `_detect_language(self)`
- `detect_language(self)`
- `language(self)`
- `_is_python_file(self)`
- `_validate_syntax(self, content)`
- `_validate_flake8(self, content)`

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `src.core.base.types.CodeLanguage.CodeLanguage`

---
*Auto-generated documentation*
