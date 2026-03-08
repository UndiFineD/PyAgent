# GraphCore

**File**: `src\classes\context\GraphCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 8 imports  
**Lines**: 109  
**Complexity**: 7 (moderate)

## Overview

GraphCore logic for PyAgent.
Pure logic for AST-based code relationship analysis and graph management.

## Classes (2)

### `CodeGraphVisitor`

**Inherits from**: NodeVisitor

AST visitor to extract imports, classes, and function calls.

**Methods** (5):
- `__init__(self, file_path)`
- `visit_Import(self, node)`
- `visit_ImportFrom(self, node)`
- `visit_ClassDef(self, node)`
- `visit_Call(self, node)`

### `GraphCore`

Pure logic for managing code relationship graphs.

**Methods** (2):
- `parse_python_content(rel_path, content)`
- `build_edges(analysis)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `ast`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Set`
- `typing.Tuple`

---
*Auto-generated documentation*
