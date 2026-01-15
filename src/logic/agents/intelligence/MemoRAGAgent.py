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

"""Agent implementing MemoRAG patterns for global context understanding.
Generates 'clues' from global memory to improve retrieval accuracy.
Ref: https://github.com/qhjqhj00/MemoRAG
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from pathlib import Path
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

__version__ = VERSION




class MemoRAGAgent(BaseAgent):
    """Memory-Augmented RAG agent for deep context discovery with sharding."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.shard_dir = Path("data/memory/agent_store/memory_shards")
        self.shard_dir.mkdir(parents=True, exist_ok=True)
        self.active_shard: str = "global"
        self._system_prompt = (
            "You are the MemoRAG Agent. "
            "You manage global context sharding. You generate 'clues' from specific "
            "memory shards to focus the fleet's attention on relevant project subspaces."
        )

    @as_tool
    def memorise_to_shard(self, context: str, shard_name: str = "global") -> None:
        """Stores context into a specific memory shard."""
        shard_file = self.shard_dir / f"{shard_name}.txt"
        with open(shard_file, "a", encoding="utf-8") as f:
            f.write(f"\n[MEM] {context}")
        logging.info(f"MemoRAG: Shard '{shard_name}' updated.")

    @as_tool
    def recall_clues_from_shard(self, query: str, shard_name: str = "global") -> list[str]:
        """Generates clues by scanning a specific memory shard."""
        shard_file = self.shard_dir / f"{shard_name}.txt"
        if not shard_file.exists():
            return [f"Notice: Shard '{shard_name}' does not exist."]

        # Simulated intelligent retrieval
        return [
            f"Clue for '{query}' in {shard_name}: Recent updates to core logic.",
            "Historical context suggests a dependency on previous Phase 40 logic."
        ]

    @as_tool
    def list_shards(self) -> list[str]:
        """Lists all existing memory shards."""
        return [f.stem for f in self.shard_dir.glob("*.txt")]

    def improve_content(self, prompt: str) -> str:
        self.list_shards()
        clues = self.recall_clues_from_shard(prompt, self.active_shard)
        return f"### MemoRAG Active Shard: {self.active_shard}\n" + "\n".join([f"- {c}" for c in clues])
