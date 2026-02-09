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


"""Agent specializing in Graph-based memory and entity relationship tracking.
Supports FalkorDB-style triple storage (Subject-Predicate-Object).
"""

from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from .mixins.graph_storage_mixin import GraphStorageMixin
from .mixins.graph_mirix_mixin import GraphMIRIXMixin
from .mixins.graph_beads_mixin import GraphBeadsMixin
from .mixins.graph_entity_mixin import GraphEntityMixin

__version__ = VERSION


# pylint: disable=too-many-ancestors
class GraphMemoryAgent(
    BaseAgent, GraphStorageMixin, GraphMIRIXMixin, GraphBeadsMixin, GraphEntityMixin
):
    """Manages long-term memories with MIRIX 6-component architecture and Beads task tracking."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.beads_dir = Path(self._workspace_root) / ".beads"
        self.beads_dir.mkdir(exist_ok=True)
        self.graph_store_path = Path(self._workspace_root) / "data/memory/agent_store/knowledge_graph.json"
        # MIRIX 6-component memory categories
        self.memory_store: Dict[str, Any] = {
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

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Graph-based reasoning helper."""
        _ = prompt
        _ = target_file
        return f"GraphMemory state: {len(self.entities)} entities, {len(self.relationships)} relationships."


if __name__ == "__main__":
    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(
        GraphMemoryAgent, "Graph Memory Agent", "Memory storage path"
    )
    main()
