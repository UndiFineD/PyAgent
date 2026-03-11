#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/ContextVisualizer.description.md

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
## Source: src-old/classes/context/ContextVisualizer.improvements.md

# Improvements for ContextVisualizer

**File**: `src\classes\context\ContextVisualizer.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 116 lines (medium)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextVisualizer_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END

"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Auto-extracted class from agent_context.py"""

import json
from pathlib import Path
from typing import Any

from src.core.base.version import VERSION
from src.logic.agents.cognitive.context.models.VisualizationData import (
    VisualizationData,
)
from src.logic.agents.cognitive.context.models.VisualizationType import (
    VisualizationType,
)

__version__ = VERSION


class ContextVisualizer:
    """Visualizes context relationships.

    Creates visual representations of context dependencies and hierarchies.

    Example:
        >>> visualizer=ContextVisualizer()
        >>> data=visualizer.create_dependency_graph(contexts)

    """

    def __init__(
        self, viz_type: VisualizationType = VisualizationType.DEPENDENCY_GRAPH
    ) -> None:
        self.viz_type: VisualizationType = viz_type
        self.nodes: list[dict[str, Any]] = []
        self.edges: list[tuple[str, str]] = []
        self.layout: str = "hierarchical"

    def set_type(self, viz_type: VisualizationType) -> None:
        self.viz_type = viz_type

    def add_node(self, node_id: str, metadata: dict[str, Any] | None = None) -> None:
        if metadata is None:
            metadata = {}
        self.nodes.append({"id": node_id, **metadata})

    def add_edge(self, source: str, target: str) -> None:
        self.edges.append((source, target))

    def generate(self) -> VisualizationData:
        return VisualizationData(
            viz_type=self.viz_type,
            nodes=self.nodes,
            edges=self.edges,
            layout=self.layout,
        )

    def export_json(self) -> str:
        data = self.generate()
        payload: dict[str, Any] = {
            "viz_type": data.viz_type.value,
            "nodes": data.nodes,
            "edges": data.edges,
            "layout": data.layout,
        }
        return json.dumps(payload)

    def create_dependency_graph(self, contexts: dict[str, str]) -> VisualizationData:
        """Create dependency graph visualization.

        Args:
            contexts: Dictionary of context file paths to contents.

        Returns:
            VisualizationData for rendering.

        """
        nodes: list[dict[str, str]] = []
        edges: list[tuple[str, str]] = []
        for path, content in contexts.items():
            nodes.append({"id": path, "label": Path(path).name})
            # Find references to other files
            for other_path in contexts.keys():
                if other_path != path:
                    other_name = Path(other_path).stem
                    if other_name in content:
                        edges.append((path, other_path))
        return VisualizationData(
            viz_type=VisualizationType.DEPENDENCY_GRAPH, nodes=nodes, edges=edges
        )

    def create_call_hierarchy(self, contexts: dict[str, str]) -> VisualizationData:
        """Create call hierarchy visualization.

        Args:
            contexts: Dictionary of context file paths to contents.

        Returns:
            VisualizationData for rendering.

        """
        nodes: list[dict[str, str]] = []
        edges: list[tuple[str, str]] = []
        for path in contexts.keys():
            nodes.append({"id": path, "label": Path(path).name})
        return VisualizationData(
            viz_type=VisualizationType.CALL_HIERARCHY,
            nodes=nodes,
            edges=edges,
            layout="tree",
        )
