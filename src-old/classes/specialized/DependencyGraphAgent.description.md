# DependencyGraphAgent

**File**: `src\classes\specialized\DependencyGraphAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 90  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for DependencyGraphAgent.

## Classes (1)

### `DependencyGraphAgent`

Maps and analyzes dependencies between agent modules and classes.
Helps in understanding the impact of changes and optimizing imports.

**Methods** (5):
- `__init__(self, workspace_path)`
- `scan_dependencies(self, start_dir)`
- `_extract_imports(self, file_path)`
- `get_impact_scope(self, module_name)`
- `generate_graph_stats(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `ast`
- `os`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Set`
- `typing.Union`

---
*Auto-generated documentation*
