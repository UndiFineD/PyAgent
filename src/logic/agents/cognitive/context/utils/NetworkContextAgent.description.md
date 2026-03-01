# NetworkContextAgent

**File**: `src\logic\agents\cognitive\context\utils\NetworkContextAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 100  
**Complexity**: 4 (simple)

## Overview

Agent that maps the codebase into a graph of relationships.

## Classes (1)

### `NetworkContextAgent`

**Inherits from**: BaseAgent

Scans the codebase to build a graph of imports and class hierarchies.

**Methods** (4):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `scan_project(self)`
- `analyze_impact(self, file_path)`

## Dependencies

**Imports** (10):
- `GraphContextEngine.GraphContextEngine`
- `logging`
- `os`
- `pathlib.Path`
- `re`
- `src.classes.base_agent.BaseAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
