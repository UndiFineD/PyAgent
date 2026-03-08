"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/system/mixins/GraphAnalysisMixin.description.md

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
## Source: src-old/logic/agents/system/mixins/GraphAnalysisMixin.improvements.md

# Improvements for GraphAnalysisMixin

**File**: `src\logic\agents\system\mixins\GraphAnalysisMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 69 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `GraphAnalysisMixin_test.py` with pytest tests

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
from src.logic.agents.system.TopologicalNavigator import TopologicalNavigator

from typing import TYPE_CHECKING, Any
from src.core.base.BaseUtilities import as_tool

class GraphAnalysisMixin:
    """Mixin for graph analysis and impact assessment in TopologicalNavigator."""

    @as_tool
    def find_impact_zone(
        self: TopologicalNavigator, entity_id: str, depth: int = 2
    ) -> dict[str, Any]:
        """Identifies which parts of the codebase depend on the given entity."""
        # Need reverse graph to find dependents
        if not self.reverse_graph:
            self._build_reverse_graph()

        affected = set()
        to_visit = [(entity_id, 0)]
        visited = set()

        while to_visit:
            current, current_depth = to_visit.pop(0)
            if current in visited or current_depth >= depth:
                continue

            visited.add(current)
            dependents = self.reverse_graph.get(current, set())
            for dep in dependents:
                affected.add(dep)
                to_visit.append((dep, current_depth + 1))

        return {
            "target": entity_id,
            "impact_zone": list(affected),
            "total_affected": len(affected),
        }

    def _build_reverse_graph(self: TopologicalNavigator) -> None:
        """Constructs the reverse dependency graph (A depends on B -> B is used by A)."""
        self.reverse_graph = {}
        for source, dependencies in self.graph.items():
            for dep in dependencies:
                if dep not in self.reverse_graph:
                    self.reverse_graph[dep] = set()
                self.reverse_graph[dep].add(source)

    @as_tool
    def get_topological_order(self: TopologicalNavigator) -> list[str]:
        """Returns nodes in topological order (safe initialization/build sequence)."""
        visited = set()
        stack = []

        def visit(node: str) -> None:
            if node not in visited:
                visited.add(node)
                for dep in self.graph.get(node, set()):
                    if dep in self.graph:
                        # Only follow internal graph
                        visit(dep)
                stack.append(node)

        for node in self.graph:
            visit(node)

        return stack[::-1]
