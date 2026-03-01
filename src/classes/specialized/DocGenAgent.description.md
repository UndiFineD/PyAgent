# DocGenAgent

**File**: `src\classes\specialized\DocGenAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 86  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for DocGenAgent.

## Classes (1)

### `DocGenAgent`

**Inherits from**: BaseAgent

Autonomous Documentation Generator: Extracts docstrings from Python modules 
and generates Markdown files compatible with Sphinx/Jekyll.

**Methods** (3):
- `__init__(self, workspace_path)`
- `extract_docs(self, file_path)`
- `generate_documentation_site(self, output_dir)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `ast`
- `os`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
