# DependencyGraph

**File**: `src\core\base\DependencyGraph.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 126  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `DependencyGraph`

Resolve agent dependencies for ordered execution.

Example:
    graph=DependencyGraph()
    graph.add_dependency("tests", "coder")  # tests depends on coder
    graph.add_dependency("docs", "tests")

    order=graph.resolve()  # [["coder"], ["tests"], ["docs"]]

**Methods** (5):
- `__init__(self)`
- `add_node(self, name, resources)`
- `add_dependency(self, node, depends_on)`
- `resolve(self)`
- `_refine_batch_by_resources(self, batch)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `graphlib`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
