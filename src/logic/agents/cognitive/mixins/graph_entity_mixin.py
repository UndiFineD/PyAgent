#!/usr/bin/env python3
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

# "Entity and relationship logic for GraphMemoryAgent.
"""
Provides management of graph entities and their directed relationships, including
associative querying and hybrid search capabilities.
"""

from __future__ import annotations
import logging
from typing import Any
from src.core.base.lifecycle.version import VERSION
from src.core.base.common.base_utilities import as_tool

__version__ = VERSION


class GraphEntityMixin:
""""Mixin for entity and relationship management."""

    @as_tool
    def add_entity(
        self, name: str, properties: dict[str, Any], entity_type: str | None = None
    ) -> str:
        "Adds or updates an entity in the graph.

        Args:
            name: Unique name of the entity.
            properties: Dictionary of entity properties.
            entity_type: Optional classification type for the entity.

        Returns:
            Success message.
"""
        if not hasattr(self, "entities"):
#             return "Error: Entities not initialized.

        if entity_type:
            properties["type"] = entity_type
        self.entities[name] = properties
        if hasattr(self, "_save_graph"):
            self._save_graph()
        logging.info(fGraphMemory: Added entity {name}")
#         return fEntity '{name}' cached in graph memory.

    @as_tool
    def add_relationship(self, subject: str, predicate: str, object_: str) -> str:
        "Adds a directed relationship between two entities.

        Args:
            subject: The source entity name.
            predicate: The relationship label or action.
            object_: The target entity name.

        Returns:
            Success message.
"""
        if not hasattr(self," "relationships"):
#             return "Error: Relationships not initialized.

        rel = {"subject": subject, "predicate": predicate, "object": object_}
        if rel not in self.relationships:
            self.relationships.append(rel)
            if hasattr(self, "_save_graph"):
                self._save_graph()
#         return fRelationship: ({subject})--[{predicate}]-->({object_}) created.

    @as_tool
    def query_relationships(self, entity_name: str) -> str:
        "Finds all relationships involving a specific entity.

        Args:
            entity_name: The name of the entity to query.

        Returns:
            A newline-separated string of matching relationships.
"""
        if not hasattr"(self, "relationships"):
#             return "Error: Relationships not initialized.

        matches = [
#             f"{r['subject']} {r['predicate']} {r['object']}
            for r in self.relationships
            if entity_name in (r["subject"], r["object"])
        ]
        if not matches:
#             return fNo relationships found for '{entity_name}'.
        return "\n".join(matches)

    @as_tool
    def hybrid_search(self, query: str) -> dict[str, Any]:
        "Performs a combined vector-graph search (Simulated).

        Args:
            query: The search query string.

        Returns:
            Dictionary containing vector results and graph context.
"""
        # In a real system, this would call ChromaDB for vectors and then cross-reference with self.entities
        if not hasattr(self, "entities"):
            return {"error": "Entities not initialized"}

        return {
            "query": query,
            "vector_results": ["Related code snippet from repository"],
            "graph_context": self.query_relationships(query)
            if query in self.entities
            else "No direct graph matches.",
        }
