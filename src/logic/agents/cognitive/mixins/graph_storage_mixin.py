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

"""Storage logic for GraphMemoryAgent.

Handles the persistence and retrieval of graph data (entities, relationships)
and 'bead' tasks from filesystem storage.
"""

from __future__ import annotations
import json
import logging
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class GraphStorageMixin:
    """Mixin for graph storage and bead persistence."""

    def _load_graph(self) -> None:
        """Loads entities and relationships from persistent storage."""
        if (
            not hasattr(self, "graph_store_path")
            or not hasattr(self, "entities")
            or not hasattr(self, "relationships")
        ):
            return

        if self.graph_store_path.exists():
            try:
                with open(self.graph_store_path, encoding="utf-8") as f:
                    data = json.load(f)
                    self.entities.update(data.get("entities", {}))
                    # Convert 'relations' from GraphRelational format to 'relationships' if needed
                    rels = data.get("relations", [])
                    for r in rels:
                        self.relationships.append(
                            {
                                "subject": r.get("source", r.get("subject")),
                                "predicate": r.get("type", r.get("predicate")),
                                "object": r.get("target", r.get("object")),
                            }
                        )
                    # Also handle if it was already in GraphMemory format
                    m_rels = data.get("relationships", [])
                    for r in m_rels:
                        if r not in self.relationships:
                            self.relationships.append(r)
            except (json.JSONDecodeError, OSError) as e:
                logging.error(f"GraphMemoryAgent: Failed to load graph: {e}")

    def _save_graph(self) -> None:
        """Persists entities and relationships to disk."""
        if (
            not hasattr(self, "graph_store_path")
            or not hasattr(self, "entities")
            or not hasattr(self, "relationships")
        ):
            return

        try:
            self.graph_store_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.graph_store_path, "w", encoding="utf-8") as f:
                json.dump(
                    {"entities": self.entities, "relationships": self.relationships},
                    f,
                    indent=4,
                )
        except OSError as e:
            logging.error(f"GraphMemoryAgent: Failed to save graph: {e}")

    def _load_beads(self) -> dict[str, dict[str, Any]]:
        """Loads tasks from .beads/ directory JSONL files."""
        tasks = {}
        if not hasattr(self, "beads_dir"):
            return tasks

        task_file = self.beads_dir / "tasks.jsonl"
        if task_file.exists():
            with open(task_file, encoding="utf-8") as f:
                for line in f:
                    try:
                        task = json.loads(line)
                        tasks[task["id"]] = task["data"]
                    except json.JSONDecodeError:
                        continue
        return tasks

    def _save_bead(self, task_id: str, data: dict[str, Any]) -> str:
        """Persists a single task to the beads JSONL (Append-only)."""
        if not hasattr(self, "beads_dir"):
            return ""

        task_file = self.beads_dir / "tasks.jsonl"
        with open(task_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({"id": task_id, "data": data}) + "\n")
        return task_id
