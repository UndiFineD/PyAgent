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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Agent specializing in Graph-based memory and entity relationship tracking.
Supports FalkorDB-style triple storage (Subject-Predicate-Object).
"""

from __future__ import annotations
from src.core.base.Version import VERSION
import logging
import json
import time
from pathlib import Path
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool

__version__ = VERSION


class GraphMemoryAgent(BaseAgent):
    """Manages long-term memories with MIRIX 6-component architecture and Beads task tracking."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.beads_dir = Path(".beads")
        self.beads_dir.mkdir(exist_ok=True)
        self.graph_store_path = Path("data/memory/agent_store/knowledge_graph.json")
        # MIRIX 6-component memory categories
        self.memory_store = {
            "core": {},  # Human/Persona identities
            "episodic": [],  # Action logs/events
            "semantic": {},  # Facts and concepts
            "procedural": {},  # Skill instructions/algorithms
            "resource": {},  # Links/Paths/Tools
            "knowledge": {},  # Synthesis/Insights
        }
        self.entities: dict[str, dict[str, Any]] = {}
        self.relationships: list[dict[str, str]] = []
        self.tasks: dict[str, dict[str, Any]] = self._load_beads()
        self.outcomes: dict[str, float] = {}
        self._load_graph()
        self._system_prompt = (
            "You are the Graph Memory Agent. "
            "You follow the MIRIX 6-component memory architecture: "
            "Core, Episodic, Semantic, Procedural, Resource, Knowledge. "
            "You apply Memory Decay over time to maintain context relevance. "
            "You manage task graphs using the Beads pattern (dependency-aware). "
            "You also maintain a persistent knowledge graph of entities and relationships."
        )

    def _load_graph(self) -> None:
        """Loads entities and relationships from persistent storage."""
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
            except Exception as e:
                logging.error(f"GraphMemoryAgent: Failed to load graph: {e}")

    def _save_graph(self) -> None:
        """Persists entities and relationships to disk."""
        try:
            self.graph_store_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.graph_store_path, "w", encoding="utf-8") as f:
                json.dump(
                    {"entities": self.entities, "relationships": self.relationships},
                    f,
                    indent=4,
                )
        except Exception as e:
            logging.error(f"GraphMemoryAgent: Failed to save graph: {e}")

    def _load_beads(self) -> dict[str, dict[str, Any]]:
        """Loads tasks from .beads/ directory JSONL files."""
        tasks = {}
        task_file = self.beads_dir / "tasks.jsonl"
        if task_file.exists():
            with open(task_file, encoding="utf-8") as f:
                for line in f:
                    try:
                        task = json.loads(line)
                        tasks[task["id"]] = task["data"]
                    except Exception:
                        continue
        return tasks

    def _save_bead(self, task_id: str, data: dict[str, Any]) -> str:
        """Persists a single task to the beads JSONL (Append-only)."""
        task_file = self.beads_dir / "tasks.jsonl"
        with open(task_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({"id": task_id, "data": data}) + "\n")

    @as_tool
    def store_mirix_memory(self, category: str, name: str, data: Any) -> str:
        """Stores a memory into one of the 6 MIRIX components."""
        if category not in self.memory_store:
            return f"Error: Category '{category}' is not a valid MIRIX component."

        entry = {
            "name": name,
            "data": data,
            "timestamp": time.time(),
            "access_count": 0,
        }

        if isinstance(self.memory_store[category], list):
            self.memory_store[category].append(entry)
        else:
            self.memory_store[category][name] = entry

        return f"Stored {name} in {category} memory store."

    @as_tool
    def decay_memories(self, threshold_score: float = 0.5) -> str:
        """Applies decay logic to all memories based on recency and utility."""
        count = 0
        now = time.time()
        # Decay logic: Score = Base_Utility / (1 + age_in_days)
        # For simplicity, we just prune memories older than 30 days that haven't been accessed.
        for category, store in self.memory_store.items():
            if isinstance(store, list):
                original_len = len(store)
                self.memory_store[category] = [
                    m
                    for m in store
                    if (now - m["timestamp"]) < (86400 * 30)
                    or m.get("access_count", 0) > 5
                ]
                count += original_len - len(self.memory_store[category])
            elif isinstance(store, dict):
                to_delete = []
                for name, m in store.items():
                    if (now - m["timestamp"]) > (86400 * 30) and m.get(
                        "access_count", 0
                    ) < 3:
                        to_delete.append(name)
                for name in to_delete:
                    del store[name]
                    count += 1

        return f"Memory Decay process complete. Pruned {count} stale memories."

    @as_tool
    def record_outcome(self, entity_id: str, success: bool) -> str:
        """Adjusts the reliability score of a memory based on user feedback (Roampal pattern)."""
        current = self.outcomes.get(entity_id, 1.0)
        delta = 0.2 if success else -0.3
        self.outcomes[entity_id] = round(max(0.0, min(2.0, current + delta)), 2)

        status = (
            "promoted"
            if self.outcomes[entity_id] > 1.5
            else "caution"
            if self.outcomes[entity_id] < 0.7
            else "stable"
        )
        logging.info(
            f"GraphMemory: Outcome for {entity_id} is {success}. New score: {self.outcomes[entity_id]}"
        )

        # Auto-prune bad advice
        if self.outcomes[entity_id] < 0.3:
            if entity_id in self.entities:
                del self.entities[entity_id]
                self._save_graph()
            return f"Memory {entity_id} deleted due to consistently poor outcomes."

        return f"Memory {entity_id} score updated to {self.outcomes[entity_id]} ({status})."

    @as_tool
    def create_task(
        self, title: str, parent_id: str | None = None, priority: int = 2
    ) -> str:
        """Creates a new task with optional parent for hierarchy (Beads pattern)."""
        task_count = len(
            [t for t in self.tasks if not parent_id or t.startswith(f"{parent_id}.")]
        )
        task_id = (
            f"{parent_id}.{task_count + 1}"
            if parent_id
            else f"epic-{len(self.tasks) + 1}"
        )

        task_data = {
            "title": title,
            "status": "ready",
            "priority": priority,
            "blocked_by": [],
            "subtasks": [],
        }
        self.tasks[task_id] = task_data

        if parent_id and parent_id in self.tasks:
            self.tasks[parent_id]["subtasks"].append(task_id)
            self._save_bead(parent_id, self.tasks[parent_id])

        self._save_bead(task_id, task_data)
        logging.info(f"GraphMemory: Created task {task_id}")
        return f"Task created: {task_id} - {title}"

    @as_tool
    def add_dependency(self, blocker_id: str, blocked_id: str) -> str:
        """Links tasks where one blocks another."""
        if blocker_id in self.tasks and blocked_id in self.tasks:
            self.tasks[blocked_id]["blocked_by"].append(blocker_id)
            self.tasks[blocked_id]["status"] = "blocked"
            self._save_bead(blocked_id, self.tasks[blocked_id])
            return f"Task {blocked_id} is now blocked by {blocker_id}."
        return "Error: One or both task IDs not found."

    @as_tool
    def compact_memory(self, threshold_days: int = 30) -> str:
        """Summarizes and prunes old closed tasks to save context (Memory Decay)."""
        closed_tasks = [
            tid for tid, t in self.tasks.items() if t["status"] == "completed"
        ]
        if not closed_tasks:
            return "No completed tasks to compact."

        summary = f"Compacted {len(closed_tasks)} tasks into a historical summary."
        # In a real impl, we'd add this to a 'history' entity
        for tid in closed_tasks:
            del self.tasks[tid]

        return summary

    @as_tool
    def add_entity(
        self, name: str, properties: dict[str, Any], entity_type: str | None = None
    ) -> str:
        """Adds or updates an entity in the graph."""
        if entity_type:
            properties["type"] = entity_type
        self.entities[name] = properties
        self._save_graph()
        logging.info(f"GraphMemory: Added entity {name}")
        return f"Entity '{name}' cached in graph memory."

    @as_tool
    def add_relationship(self, subject: str, predicate: str, object_: str) -> str:
        """Adds a directed relationship between two entities."""
        rel = {"subject": subject, "predicate": predicate, "object": object_}
        if rel not in self.relationships:
            self.relationships.append(rel)
            self._save_graph()
        return f"Relationship: ({subject})--[{predicate}]-->({object_}) created."

    @as_tool
    def query_relationships(self, entity_name: str) -> str:
        """Finds all relationships involving a specific entity."""
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

        return {
            "query": query,
            "vector_results": ["Related code snippet from repository"],
            "graph_context": self.query_relationships(query)
            if query in self.entities
            else "No direct graph matches.",
        }

    def improve_content(self, prompt: str) -> str:
        """Graph-based reasoning helper."""
        return f"GraphMemory state: {len(self.entities)} entities, {len(self.relationships)} relationships."


if __name__ == "__main__":
    from src.core.base.BaseUtilities import create_main_function

    main = create_main_function(
        GraphMemoryAgent, "Graph Memory Agent", "Memory storage path"
    )
    main()
