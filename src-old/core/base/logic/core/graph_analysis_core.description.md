# graph_analysis_core

**File**: `src\core\base\logic\core\graph_analysis_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 150  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for graph_analysis_core.

## Classes (1)

### `GraphAnalysisCore`

Core for graph-based security and relationship analysis.

**Methods** (7):
- `__init__(self, storage_path)`
- `create_graph(self, graph_id, nodes, edges)`
- `_build_adjacency_list(self, edges)`
- `find_shortest_paths(self, graph_id, start, end)`
- `detect_cycles(self, graph_id)`
- `analyze_privilege_escalation_paths(self, graph_id, user_node)`
- `export_graph(self, graph_id, format)`

## Dependencies

**Imports** (8):
- `collections.defaultdict`
- `json`
- `os`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`

---
*Auto-generated documentation*
