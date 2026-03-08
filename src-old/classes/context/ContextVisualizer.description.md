# ContextVisualizer

**File**: `src\classes\context\ContextVisualizer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 116  
**Complexity**: 8 (moderate)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextVisualizer`

Visualizes context relationships.

Creates visual representations of context dependencies and hierarchies.

Example:
    >>> visualizer=ContextVisualizer()
    >>> data=visualizer.create_dependency_graph(contexts)

**Methods** (8):
- `__init__(self, viz_type)`
- `set_type(self, viz_type)`
- `add_node(self, node_id, metadata)`
- `add_edge(self, source, target)`
- `generate(self)`
- `export_json(self)`
- `create_dependency_graph(self, contexts)`
- `create_call_hierarchy(self, contexts)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `json`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.models.VisualizationData.VisualizationData`
- `src.logic.agents.cognitive.context.models.VisualizationType.VisualizationType`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
