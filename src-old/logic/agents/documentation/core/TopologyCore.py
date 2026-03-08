
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/documentation/core/TopologyCore.description.md

# TopologyCore

**File**: `src\logic\agents\documentation\core\TopologyCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 52  
**Complexity**: 2 (simple)

## Overview

Core logic for Swarm Topology Generation (Phase 169).
This module is designed to be side-effect free and a candidate for Rust acceleration.

## Classes (1)

### `TopologyCore`

Class TopologyCore implementation.

**Methods** (2):
- `generate_mermaid_graph(nodes, edges, direction)`
- `filter_active_relationships(all_deps, focus_list)`

## Dependencies

**Imports** (2):
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/documentation/core/TopologyCore.improvements.md

# Improvements for TopologyCore

**File**: `src\logic\agents\documentation\core\TopologyCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 52 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: TopologyCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TopologyCore_test.py` with pytest tests

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

"""
Core logic for Swarm Topology Generation (Phase 169).
This module is designed to be side-effect free and a candidate for Rust acceleration.
"""

from typing import Dict, List

class TopologyCore:
    @staticmethod
    def generate_mermaid_graph(nodes: list[str], edges: list[dict[str, str]], direction: str = "TD") -> str:
        """
        Generates a Mermaid.js flowchart string.
        :param nodes: List of node names.
        :param edges: List of dicts with 'from', 'to', and optional 'label'.
        :param direction: Mermaid direction (TD, LR, etc.)
        :return: A mermaid formatted string.
        """
        lines = [f"graph {direction}"]
        
        # Add nodes with basic styling based on type
        for node in nodes:
            safe_id = node.replace(".", "_").replace("/", "_").replace("\\", "_")
            if "Agent" in node:
                lines.append(f"    {safe_id}([{node}])")
            elif "Core" in node:
                lines.append(f"    {safe_id}{{{{{node}}}}}")
            else:
                lines.append(f"    {safe_id}[{node}]")
                
        # Add edges
        for edge in edges:
            u = edge['from'].replace(".", "_").replace("/", "_").replace("\\", "_")
            v = edge['to'].replace(".", "_").replace("/", "_").replace("\\", "_")
            label = edge.get('label', '')
            if label:
                lines.append(f"    {u} -->|{label}| {v}")
            else:
                lines.append(f"    {u} --> {v}")
                
        return "\n".join(lines)

    @staticmethod
    def filter_active_relationships(all_deps: dict[str, list[str]], focus_list: list[str]) -> dict[str, list[str]]:
        """
        Filters a dependency map to only include nodes relevant to the focus list.
        """
        filtered = {}
        for source, targets in all_deps.items():
            if any(f in source for f in focus_list):
                filtered[source] = [t for t in targets if any(f in t for f in focus_list) or "Core" in t]
        return filtered