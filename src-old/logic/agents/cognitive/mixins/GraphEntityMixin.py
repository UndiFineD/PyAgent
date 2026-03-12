#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/mixins/GraphEntityMixin.description.md

# GraphEntityMixin

**File**: `src\logic\agents\cognitive\mixins\GraphEntityMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 82  
**Complexity**: 4 (simple)

## Overview

Entity and relationship logic for GraphMemoryAgent.

## Classes (1)

### `GraphEntityMixin`

Mixin for entity and relationship management.

**Methods** (4):
- `add_entity(self, name, properties, entity_type)`
- `add_relationship(self, subject, predicate, object_)`
- `query_relationships(self, entity_name)`
- `hybrid_search(self, query)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseUtilities.as_tool`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/mixins/GraphEntityMixin.improvements.md

# Improvements for GraphEntityMixin

**File**: `src\logic\agents\cognitive\mixins\GraphEntityMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 82 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `GraphEntityMixin_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

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

"""Entity and relationship logic for GraphMemoryAgent."""

import logging
from typing import Any
from src.core.base.BaseUtilities import as_tool


class GraphEntityMixin:
    """Mixin for entity and relationship management."""

    @as_tool
    def add_entity(
        self, name: str, properties: dict[str, Any], entity_type: str | None = None
    ) -> str:
        """Adds or updates an entity in the graph."""
        if not hasattr(self, "entities"):
            return "Error: Entities not initialized."

        if entity_type:
            properties["type"] = entity_type
        self.entities[name] = properties
        if hasattr(self, "_save_graph"):
            self._save_graph()
        logging.info(f"GraphMemory: Added entity {name}")
        return f"Entity '{name}' cached in graph memory."

    @as_tool
    def add_relationship(self, subject: str, predicate: str, object_: str) -> str:
        """Adds a directed relationship between two entities."""
        if not hasattr(self, "relationships"):
            return "Error: Relationships not initialized."

        rel = {"subject": subject, "predicate": predicate, "object": object_}
        if rel not in self.relationships:
            self.relationships.append(rel)
            if hasattr(self, "_save_graph"):
                self._save_graph()
        return f"Relationship: ({subject})--[{predicate}]-->({object_}) created."

    @as_tool
    def query_relationships(self, entity_name: str) -> str:
        """Finds all relationships involving a specific entity."""
        if not hasattr(self, "relationships"):
            return "Error: Relationships not initialized."

        matches = [
            f"{r['subject']} {r['predicate']} {r['object']}"
            for r in self.relationships
            if r["subject"] == entity_name or r["object"] == entity_name
        ]
        if not matches:
            return f"No relationships found for '{entity_name}'."
        return "\n".join(matches)

    @as_tool
    def hybrid_search(self, query: str) -> dict[str, Any]:
        """Performs a combined vector-graph search (Simulated)."""
        # In a real system, this would call ChromaDB for vectors and then cross-reference with self.entities
        if not hasattr(self, "entities"):
            return {"error": "Entities not initialized"}

        return {
            "query": query,
            "vector_results": ["Related code snippet from repository"],
            "graph_context": (
                self.query_relationships(query)
                if query in self.entities
                else "No direct graph matches."
            ),
        }
