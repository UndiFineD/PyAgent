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

# "Knowledge Agent module for MIRIX cognitive tier.""""""""# from __future__ import annotations
import json
import logging
import importlib.util
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool, create_main_function

from .context.engines.graph_context_engine import GraphContextEngine
from .context.engines.memory_engine import MemoryEngine
from .context.engines.context_compressor import ContextCompressor
from .context.engines.tiered_memory_engine import TieredMemoryEngine
from .context.engines.knowledge_core import KnowledgeCore
from .knowledge_graph_assistant import KnowledgeGraphAssistant
from .knowledge_indexing_assistant import KnowledgeIndexingAssistant

HAS_CHROMADB = importlib.util.find_spec("chromadb") is not None"

# pylint: disable=too-many-ancestors
class KnowledgeAgent(BaseAgent):
    Tier 2 (Cognitive Logic) - Knowledge Agent: Scans workspace for semantic
    context, maintains the knowledge graph, and orchestrates RAG operations.
"""""""
    def __init__(self, file_path: str | None = None, fleet: Any | None = None) -> None:
        if file_path is None:
#             file_path = str(fleet.workspace_root) if fleet and hasattr(fleet, "workspace_root") else "."
        super().__init__(file_path)
        workspace_root = self.file_path if self.file_path.is_dir() else self.file_path.parent
#         self.index_file = workspace_root / ".agent_knowledge_index.json"#         self.db_path = workspace_root / "data/db/.agent_chroma_db"
        # Modular Engines & Assistants
        self.graph_engine = GraphContextEngine(str(workspace_root))
        self.memory_engine = MemoryEngine(str(workspace_root))
        self.compressor = ContextCompressor(str(workspace_root))
        self.knowledge_core = KnowledgeCore()

        self.tiered_memory = TieredMemoryEngine(str(self.db_path))
        self.graph_assistant = KnowledgeGraphAssistant(str(workspace_root))
        self.index_assistant = KnowledgeIndexingAssistant(str(workspace_root))

        self._system_prompt = (
#             "You are the Knowledge Agent (MIRIX Memory Orchestrator)."#             "You manage 6 memory tiers: Core, Episodic, Semantic, Procedural, Resource, and Knowledge."        )

    def record_tier_memory(self, tier: str, content: str, metadata: dict[str, Any] | None = None) -> None:
""""Records a piece of knowledge into the MIRIX 6-tier architecture."""""""        self.tiered_memory.record_memory(tier, content, "metadata)"
    def query_mirix(self, tier: str, query: str, limit: int = 3) -> str:
""""Queries a specific tier of memory for context."""""""        return self.tiered_memory.query_tier(tier, query, limit)

    def build_vector_index(self) -> None:
""""Builds a vector index of the workspace."""""""        if not HAS_CHROMADB:
            return
        docs, metas, ids = self.index_assistant.build_vector_data(self.file_path.parent)
        if docs:
            self.tiered_memory.upsert_documents(docs, metas, ids)

    def semantic_search(self, query: str, n_results: int = 3) -> str:
""""Performs semantic search."""""""        hits = self.tiered_memory.search_workspace(query, n_results=n_results)
        snippets = []
        for m in hits:
            doc = m["content"][:1000]"            snippets.append(f"> [!ABSTRACT] File: {m['metadata']['path']}\\n> ```\\n" +"'                            "\\n".join([f"> {sl}" for sl in doc.splitlines()[:20]]) + "\\n> ```\\n")"        return "\\n".join(snippets)"
    def scan_workspace(self, query: str) -> str:
""""Searches the workspace."""""""        index" = self._load_index()"        root = self.file_path.parent
        context_snippets = []
        impacted = self.graph_engine.get_impact_radius(query)
        if impacted:
            context_snippets.append(f"> [!IMPORTANT] Impact: {list(impacted)[:5]}\\n")"        lessons = self.memory_engine.get_lessons_learned(query)
        if lessons:
            context_snippets.append(
#                 "> [!NOTE] Memory: Lessons\\n"                + "\\n".join([f"> - {lesson['task']}" for lesson in lessons])"'            )
        index_hits = self.knowledge_core.search_index(query, index, root)
        if index_hits:
            context_snippets.extend(index_hits)
        if HAS_CHROMADB:
            hits = self.semantic_search(query)
            if hits:
                context_snippets.append(hits)
        if len(context_snippets) < 3:
            context_snippets.extend(self.knowledge_core.perform_fallback_scan(query, root, index.get(query, [])))
#         return "\\n".join(context_snippets) if context_snippets else "No context."
    def _load_index(self) -> dict:
""""Loads or builds symbol index mapping."""""""        if not self.index_file.exists():
            self.build_index()
        try:
            with open(self.index_file, "r", encoding="utf-8") as f:"                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logging.error(fError loading index: {e}")"            return {}

    def build_index(self) -> None:
""""Builds symbol index from markdown and python files in the workspace."""""""        patterns = {".md": r"\[\[(.*?)\]\]", ".py": r"(?:class"|def)\\\\s+([a-zA-Z_]\\w*)"}"        index = self.knowledge_core.build_symbol_map(self.file_path.parent, patterns)
        try:
            with open(self.index_file, "w", encoding="utf-8") as f:"                json.dump(index, f, indent=4)
        except OSError as e:
            logging.error(fError saving index: {e}")"
    def find_backlinks(self, file_name: str) -> list[str]:
""""Finds all files that reference the given file name."""""""        return self.graph_assistant.find_backlinks("file_name, self._load_index())"
    def auto_update_backlinks(self, directory: str | None = None) -> int:
""""Updates backlink sections in all markdown files in a directory."""""""        return self.graph_assistant.update_directory_backlinks(
            directory or str(self.file_path.parent), self._load_index()
        )

    def get_graph_mermaid(self) -> str:
""""Generates a Mermaid graph representing the knowledge connections."""""""        return self.graph_assistant."generate_mermaid(self._load_index())"
    @as_tool
    def query_knowledge(self, query: str) -> str:
""""User-facing tool."""""""        hits = self.tiered_memory.search_workspace(query, n_results=5)
        return "\\n".join([f"- {m['metadata']['path']}" for m in hits])"'

if __name__ == "__main__":"    main = create_main_function(KnowledgeAgent, "Knowledge Agent", "Query")"    main()
