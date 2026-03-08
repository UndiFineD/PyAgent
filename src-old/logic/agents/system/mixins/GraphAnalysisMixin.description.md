# GraphAnalysisMixin

**File**: `src\logic\agents\system\mixins\GraphAnalysisMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 69  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for GraphAnalysisMixin.

## Classes (1)

### `GraphAnalysisMixin`

Mixin for graph analysis and impact assessment in TopologicalNavigator.

**Methods** (3):
- `find_impact_zone(self, entity_id, depth)`
- `_build_reverse_graph(self)`
- `get_topological_order(self)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `src.core.base.BaseUtilities.as_tool`
- `src.logic.agents.system.TopologicalNavigator.TopologicalNavigator`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
