# GraphContextEngine

**File**: `src\classes\context\GraphContextEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 126  
**Complexity**: 6 (moderate)

## Overview

Core engine for managing code relationships as a graph.

## Classes (1)

### `GraphContextEngine`

Manages an adjacency list of file and class dependencies.

**Methods** (6):
- `__init__(self, workspace_root)`
- `add_edge(self, source, target, relationship)`
- `scan_project(self, start_path)`
- `get_impact_radius(self, node, max_depth)`
- `save(self)`
- `load(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.engines.GraphCore.GraphCore`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
