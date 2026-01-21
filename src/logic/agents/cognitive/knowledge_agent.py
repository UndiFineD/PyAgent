#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Refactored for < 50 Complexity

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import create_main_function, as_tool
from src.logic.agents.cognitive.context.engines.graph_context_engine import (
    GraphContextEngine,
)
from src.logic.agents.cognitive.context.engines.memory_engine import MemoryEngine
from src.logic.agents.cognitive.context.engines.context_compressor import (
    ContextCompressor,
)
from src.logic.agents.cognitive.context.engines.knowledge_core import KnowledgeCore
from src.logic.agents.cognitive.context.engines.tiered_memory_engine import (
    TieredMemoryEngine,
)
from src.logic.agents.cognitive.knowledge_graph_assistant import KnowledgeGraphAssistant
from src.logic.agents.cognitive.knowledge_indexing_assistant import (
    KnowledgeIndexingAssistant,
)
import json
from typing import Any

__version__ = VERSION

import importlib.util
HAS_CHROMADB = importlib.util.find_spec("chromadb") is not None


class KnowledgeAgent(BaseAgent):
    """
    Tier 2 (Cognitive Logic) - Knowledge Agent: Scans workspace for semantic 
    context, maintains the knowledge graph, and orchestrates RAG operations.
    """

    def __init__(self, file_path: str | None = None, fleet: Any | None = None) -> None:
        if file_path is None:
            file_path = str(fleet.workspace_root) if fleet and hasattr(fleet, "workspace_root") else "."

        super().__init__(file_path)
        workspace_root = self.file_path if self.file_path.is_dir() else self.file_path.parent
        self.index_file = workspace_root / ".agent_knowledge_index.json"
        self.db_path = workspace_root / "data/db/.agent_chroma_db"

        # Modular Engines & Assistants
        self.graph_engine = GraphContextEngine(str(workspace_root))
        self.memory_engine = MemoryEngine(str(workspace_root))
        self.compressor = ContextCompressor(str(workspace_root))
        self.knowledge_core = KnowledgeCore()

        self.tiered_memory = TieredMemoryEngine(str(self.db_path))
        self.graph_assistant = KnowledgeGraphAssistant(str(workspace_root))
        self.index_assistant = KnowledgeIndexingAssistant(str(workspace_root))

        self._system_prompt = (
            "You are the Knowledge Agent (MIRIX Memory Orchestrator). "
            "You manage 6 memory tiers: Core, Episodic, Semantic, Procedural, Resource, and Knowledge."
        )

    def record_tier_memory(self, tier: str, content: str, metadata: dict[str, Any] | None = None) -> None:
        """Records a piece of knowledge into the MIRIX 6-tier architecture."""
        self.tiered_memory.record_memory(tier, content, metadata)

    def query_mirix(self, tier: str, query: str, limit: int = 3) -> str:
        """Queries a specific tier of memory for context."""
        return self.tiered_memory.query_tier(tier, query, limit)

    def build_vector_index(self) -> None:
        """Builds a vector index of the workspace."""
        if not HAS_CHROMADB:
            return
        docs, metas, ids = self.index_assistant.build_vector_data(self.file_path.parent)
        if docs:
            self.tiered_memory.upsert_documents(docs, metas, ids)

    def semantic_search(self, query: str, n_results: int = 3) -> str:
        """Performs semantic search."""
        hits = self.tiered_memory.search_workspace(query, n_results=n_results)
        snippets = []
        for m in hits:
            doc = m["content"][:1000]
            snippets.append(f"> [!ABSTRACT] File: {m['metadata']['path']}\n> ```\n" +
                           "\n".join([f"> {sl}" for sl in doc.splitlines()[:20]]) + "\n> ```\n")
        return "\n".join(snippets)

    def scan_workspace(self, query: str) -> str:
        """Searches the workspace."""
        index = self._load_index()
        root = self.file_path.parent
        context_snippets = []
        impacted = self.graph_engine.get_impact_radius(query)
        if impacted:
            context_snippets.append(f"> [!IMPORTANT] Impact: {list(impacted)[:5]}\n")
        lessons = self.memory_engine.get_lessons_learned(query)
        if lessons:
            context_snippets.append(
                "> [!NOTE] Memory: Lessons\n"
                + "\n".join([f"> - {lesson['task']}" for lesson in lessons])
            )
        index_hits = self.knowledge_core.search_index(query, index, root)
        if index_hits:
            context_snippets.extend(index_hits)
        if HAS_CHROMADB:
            hits = self.semantic_search(query)
            if hits:
                context_snippets.append(hits)
        if len(context_snippets) < 3:
            context_snippets.extend(self.knowledge_core.perform_fallback_scan(query, root, index.get(query, [])))
        return "\n".join(context_snippets) if context_snippets else "No context."

    def _load_index(self) -> dict:
        """Loads or builds symbols."""
        if not self.index_file.exists():
            self.build_index()
        try:
            with open(self.index_file) as f:
                return json.load(f)
        except Exception:
            return {}

    def build_index(self) -> None:
        """Builds symbol index."""
        patterns = {".md": r"\[\[(.*?)\]\]", ".py": r"(?:class|def)\s+([a-zA-Z_]\w*)"}
        index = self.knowledge_core.build_symbol_map(self.file_path.parent, patterns)
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4)

    def find_backlinks(self, file_name: str) -> list[str]:
        return self.graph_assistant.find_backlinks(file_name, self._load_index())

    def auto_update_backlinks(self, directory: str | None = None) -> int:
        return self.graph_assistant.update_directory_backlinks(directory or str(self.file_path.parent), self._load_index())

    def get_graph_mermaid(self) -> str:
        return self.graph_assistant.generate_mermaid(self._load_index())

    @as_tool
    def query_knowledge(self, query: str) -> str:
        """User-facing tool."""
        hits = self.tiered_memory.search_workspace(query, n_results=5)
        return "\n".join([f"- {m['metadata']['path']}" for m in hits])

if __name__ == "__main__":
    main = create_main_function(KnowledgeAgent, "Knowledge Agent", "Query")
    main()

