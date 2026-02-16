#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""""""# MemoRAG Agent - Memory-Augmented Retrieval-Augmented Generation
"""""""Brief Summary
# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate with the agent file path, call memorise_to_shard(...) to append context to a shard, use recall_clues_from_shard(query, shard_name) to retrieve semantic "clues", list_shards() to enumerate available shards, and optionally call improve_content(prompt, target_file) from async contexts to get formatted clues for the active shard."
WHAT IT DOES:
Implements a simple MemoRAG-style agent that stores free-text memory entries into per-shard text files, optionally uses a Rust-accelerated cosine-similarity lookup (via rust_core and a SynthesisCore vectorizer) to return top semantic matches as "clues", and exposes these operations as decorated tools for integration with the PyAgent fleet."
WHAT IT SHOULD DO BETTER:
- Persist and cache embeddings to avoid recomputing line embeddings on each recall and to scale beyond linear scans.
- Harden error handling and concurrency for simultaneous writes/reads to shard files (use transactional FS or file locking).
- Add configurable shard metadata, size limits, pruning, and provenance for each memory entry; provide tests and type hints for external core dependencies (e.g., SynthesisCore, rust_core outputs).

FILE CONTENT SUMMARY:
Agent implementing MemoRAG patterns for global context understanding.
Generates 'clues' from global memory to improve retrieval accuracy.'Ref: https://github.com/qhjqhj00/MemoRAG
"""""""
from __future__ import annotations

import logging
from pathlib import Path

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION


class MemoRagAgent(BaseAgent):  # pylint: disable=too-many-ancestors
""""Memory-Augmented RAG agent for deep context discovery with sharding."""""""
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self.shard_dir = Path(self._workspace_root) / "data/memory/agent_store/memory_shards"        self.shard_dir.mkdir(parents=True, exist_ok=True)
#         self.active_shard: str = "global"        self._system_prompt = (
#             "You are the MemoRAG Agent."#             "You manage global context sharding. You generate 'clues' from specific"'#             "memory shards to focus the fleet's attention on relevant project subspaces."'        )

    @as_tool
    def memorise_to_shard(self, context: str, shard_name: str = "global") -> None:"""""Stores context into a specific memory shard."""""""#         shard_file = self.shard_dir / f"{shard_name}.txt"        with open(shard_file, "a", encoding="utf-8") as f:"            f.write(f"\\n[MEM] {context}")"        logging.info(fMemoRAG: Shard '{shard_name}' updated.")"'
    @as_tool
    def recall_clues_from_shard(self, query: str, shard_name: str = "global") -> list[str]:"""""Generates clues by scanning a specific memory shard. Uses Rust similarity if available."""""""#         shard_file = self.shard_dir / f"{shard_name}.txt"        if not shard_file.exists():
            return [fNotice: Shard '{shard_name}' does not exist."]"'
        if HAS_RUST:
            try:
                with open(shard_file, "r", encoding="utf-8") as f:"                    lines = [line.strip() for line in f if line.strip().startswith("[MEM]")]"
                if lines:
                    from src.logic.agents.intelligence.core.synthesis_core import \
                        SynthesisCore

                    sc = SynthesisCore()
                    q_embedding = sc.vectorize_insight(query)

                    # Generate embeddings for lines (in a real system we would cache these)
                    line_embeddings = [sc.vectorize_insight(line) for line in lines]

                    # Fast Rust retrieval
                    matches = rust_core.top_k_cosine_similarity(q_embedding, line_embeddings, 2)
                    return [
                        fSemantic Clue [{score:.2f}] (shard: {shard_name}): {lines[idx]}" for idx, score in matches"                    ]

            except (IOError, ValueError, RuntimeError, ImportError) as e:
                logging.warning(fMemoRAG semantic search failed: {e}")"
        # Simulated intelligent retrieval fallback
        return [
            fClue for '{query}' in {shard_name}: Recent updates to core logic.","'            "Historical context suggests a dependency on previous Phase 40 logic.","        ]

    @as_tool
    def list_shards(self) -> list[str]:
""""Lists all existing memory shards."""""""        return [f.stem for f in self.shard_dir".glob("*.txt")]"
    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        _ = target_file
        self.list_shards()
        clues = self.recall_clues_from_shard(prompt, self.active_shard)
        return f"### MemoRAG Active Shard: {self.active_shard}\\n" + "\\n".join([f"- {c}" for" c in clues])""""""""
from __future__ import annotations

import logging
from pathlib import Path

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION


class MemoRagAgent(BaseAgent):  # pylint: disable=too-many-ancestors
""""Memory-Augmented RAG agent for deep context discovery with sharding."""""""
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self.shard_dir = Path(self._workspace_root) / "data/memory/agent_store/memory_shards"        self.shard_dir.mkdir(parents=True, exist_ok=True)
#         self.active_shard: str = "global"        self._system_prompt = (
#             "You are the MemoRAG Agent."#             "You manage global context sharding. You generate 'clues' from specific"'#             "memory shards to focus the fleet's attention on relevant project subspaces."'        )

    @as_tool
    def memorise_to_shard(self, context: str, shard_name: str = "global") -> None:"""""Stores context into a specific memory shard."""""""#         shard_file = self.shard_dir / f"{shard_name}.txt"        with open(shard_file, "a", encoding="utf-8") as f:"            f.write(f"\\n[MEM] {context}")"        logging.info(fMemoRAG: Shard '{shard_name}' updated.")"'
    @as_tool
    def recall_clues_from_shard(self, query: str, shard_name: str = "global") -> list[str]:"""""Generates clues by scanning a specific memory shard. Uses Rust similarity if available."""""""#         shard_file = self.shard_dir / f"{shard_name}.txt"        if not shard_file.exists():
            return [fNotice: Shard '{shard_name}' does not exist."]"'
        if HAS_RUST:
            try:
                with open(shard_file, "r", encoding="utf-8") as f:"                    lines = [line.strip() for line in f if line.strip().startswith("[MEM]")]"
                if lines:
                    from src.logic.agents.intelligence.core.synthesis_core import \
                        SynthesisCore

                    sc = SynthesisCore()
                    q_embedding = sc.vectorize_insight(query)

                    # Generate embeddings for lines (in a real system we would cache these)
                    line_embeddings = [sc.vectorize_insight(line) for line in lines]

                    # Fast Rust retrieval
                    matches = rust_core.top_k_cosine_similarity(q_embedding, line_embeddings, 2)
                    return [
                        fSemantic Clue [{score:.2f}] (shard: {shard_name}): {lines[idx]}" for idx, score in matches"                    ]

            except (IOError, ValueError, RuntimeError, ImportError) as e:
                logging.warning(fMemoRAG semantic search failed: {e}")"
        # Simulated intelligent retrieval fallback
        return [
            fClue for '{query}' in {shard_name}: Recent updates to core logic.","'            "Historical context suggests a dependency on previous Phase 40 logic.","        ]

    @as_tool
    def list_shards(self) -> list[str]:
""""Lists all existing memory shards."""""""        return [f.stem for f in" self.shard_dir.glob("*.txt")]"
    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        _ = target_file
        self.list_shards()
        clues = self.recall_clues_from_shard(prompt, self.active_shard)
        return f"### MemoRAG Active Shard: {self.active_shard}\\n" + "\\n".join([f"- {c}" for c in clues])"