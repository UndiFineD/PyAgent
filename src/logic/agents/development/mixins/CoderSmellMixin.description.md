# CoderSmellMixin

**File**: `src\logic\agents\development\mixins\CoderSmellMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 154  
**Complexity**: 5 (moderate)

## Overview

Code smell detection logic for CoderCore.

## Classes (1)

### `CoderSmellMixin`

Mixin for detecting code smells.

**Methods** (5):
- `detect_code_smells(self, content)`
- `_detect_python_smells(self, content)`
- `_check_python_method_smells(self, node, smells)`
- `_check_python_class_smells(self, node, smells)`
- `_detect_generic_smells(self, content)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `ast`
- `src.core.base.types.CodeLanguage.CodeLanguage`
- `src.core.base.types.CodeSmell.CodeSmell`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
