# KnowledgeGraphAssistant

**File**: `src\logic\agents\cognitive\KnowledgeGraphAssistant.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 46  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for KnowledgeGraphAssistant.

## Classes (1)

### `KnowledgeGraphAssistant`

Handles backlinks, dependency tracking, and graph visualization.

**Methods** (5):
- `__init__(self, workspace_root)`
- `get_impact_radius(self, query)`
- `find_backlinks(self, target_file, index)`
- `generate_mermaid(self, index)`
- `generate_mermaid_graph(self)`

## Dependencies

**Imports** (2):
- `pathlib.Path`
- `typing.Set`

---
*Auto-generated documentation*
