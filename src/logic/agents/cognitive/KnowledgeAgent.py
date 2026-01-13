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

"""Agent specializing in Workspace Knowledge and Codebase Context (RAG-lite)."""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function, as_tool
from src.logic.agents.cognitive.context.engines.GraphContextEngine import GraphContextEngine
from src.logic.agents.cognitive.context.engines.MemoryEngine import MemoryEngine
from src.logic.agents.cognitive.context.engines.ContextCompressor import ContextCompressor
from src.logic.agents.cognitive.context.engines.KnowledgeCore import KnowledgeCore
import logging
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

__version__ = VERSION

try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False

class KnowledgeAgent(BaseAgent):
    """Agent that scans the workspace to provide deep context using MIRIX 6-tier memory."""
    
    def __init__(self, file_path: str | None = None, fleet: Any | None = None) -> None:
        # Phase 123: Robust initialization for dynamic discovery
        if file_path is None:
             if fleet and hasattr(fleet, "workspace_root"):
                 file_path = str(fleet.workspace_root)
             else:
                 file_path = "."
        
        super().__init__(file_path)
        workspace_root = self.file_path if self.file_path.is_dir() else self.file_path.parent
        self.index_file = workspace_root / ".agent_knowledge_index.json"
        self.db_path = workspace_root / "data/db/.agent_chroma_db"
        self._chroma_client = None
        self._collection = None  # Standard Knowledge collection
        self._mirix_collection = None # MIRIX Tiered collection
        self.graph_engine = GraphContextEngine(str(workspace_root))
        self.memory_engine = MemoryEngine(str(workspace_root))
        self.compressor = ContextCompressor(str(workspace_root))
        self.knowledge_core = KnowledgeCore()
        
        self._system_prompt = (
            "You are the Knowledge Agent (MIRIX Memory Orchestrator). "
            "You manage 6 memory tiers: Core, Episodic, Semantic, Procedural, Resource, and Knowledge. "
            "Your role is to retrieve high-utility context to prevent the team from repeating past failures (Outcome Learning). "
            "Provide detailed summaries using Obsidian-style callouts."
        )

    def _init_chroma(self) -> bool:
        """Initialize ChromaDB client and multiple collections for tiered memory."""
        if not HAS_CHROMADB:
            return False
        
        try:
            if self._chroma_client is None:
                self._chroma_client = chromadb.PersistentClient(path=str(self.db_path))
                self._collection = self._chroma_client.get_or_create_collection(name="workspace_docs")
                self._mirix_collection = self._chroma_client.get_or_create_collection(name="mirix_tiers")
            return True
        except Exception as e:
            logging.error(f"ChromaDB init error: {e}")
            return False

    def build_index(self) -> str:
        """Builds a symbol and backlink index for the workspace via knowledge_core."""
        root = self.file_path.parent
        patterns = {
            ".md": r"\[\[(.*?)\]\]",
            ".py": r"(?:class|def)\s+([a-zA-Z_][a-zA-Z0-9_]*)"
        }
        index = self.knowledge_core.build_symbol_map(root, patterns)
                
        with open(self.index_file, "w") as f:
            json.dump(index, f, indent=4)
        logging.info(f"Knowledge index built at {self.index_file}")

    def record_tier_memory(self, tier: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Records a piece of knowledge into the MIRIX 6-tier architecture.
        Tiers: core, episodic, semantic, procedural, resource, knowledge.
        """
        if not self._init_chroma():
            return
        
        valid_tiers = ["core", "episodic", "semantic", "procedural", "resource", "knowledge"]
        if tier.lower() not in valid_tiers:
            logging.warning(f"Invalid MIRIX tier: {tier}")
        
        meta = metadata or {}
        meta["tier"] = tier.lower()
        meta["timestamp"] = datetime.now().isoformat()
        
        try:
            self._mirix_collection.add(
                documents=[content],
                metadatas=[meta],
                ids=[f"{tier}_{int(datetime.now().timestamp())}"]
            )
        except Exception as e:
            logging.error(f"MIRIX record error: {e}")

    def query_mirix(self, tier: str, query: str, limit: int = 3) -> str:
        """Queries a specific tier of memory for context."""
        if not self._init_chroma():
            return ""
        
        try:
            results = self._mirix_collection.query(
                query_texts=[query],
                n_results=limit,
                where={"tier": tier.lower()}
            )
            
            output = [f"### [MIRIX Tier: {tier.upper()}] Results for '{query}'"]
            for i, doc in enumerate(results.get("documents", [[]])[0]):
                output.append(f"> [!NOTE] Memory {i+1}\n> {doc}\n")
            return "\n".join(output)
        except Exception as e:
            logging.error(f"MIRIX query error: {e}")
            return f"Error querying {tier} memory."

    def build_vector_index(self) -> str:
        """Builds a vector index of the workspace for semantic search."""
        if not self._init_chroma():
            logging.warning("Skipping vector index: ChromaDB not available.")
            return

        root = self.file_path.parent
        documents = []
        metadatas = []
        ids = []

        count = 0
        for p in root.rglob("*"):
            if p.is_dir() or p.suffix not in [".py", ".md", ".txt"]:
                continue
            if any(part in str(p) for part in ["__pycache__", "venv", ".git", "data/db/.agent_chroma_db"]):
                continue
            
            try:
                content = p.read_text(encoding="utf-8")
                if not content.strip():
                    continue
                
                # Chunking: for now simple line-based or whole file
                # To keep it simple for a "quick implementation", we'll do file-level with some overlap if large
                # But let's just do file-level for now.
                documents.append(content)
                metadatas.append({"path": str(p.relative_to(root))})
                ids.append(str(p.relative_to(root)))
                count += 1
            except Exception as e:
                logging.error(f"Error reading {p} for vector index: {e}")

        if documents:
            self._collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logging.info(f"Vector index built with {count} documents.")

    def semantic_search(self, query: str, n_results: int = 3) -> str:
        """Performs semantic search using ChromaDB."""
        if not self._init_chroma():
            return ""

        try:
            results = self._collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            snippets = []
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i]
                path = meta['path']
                
                # Truncate doc if too long
                if len(doc) > 1000:
                    doc = doc[:1000] + "\n... (truncated)"
                
                snippets.append(f"> [!ABSTRACT] File: {path} (Semantic Match)\n> ```\n" + "\n".join([f"> {sl}" for sl in doc.splitlines()[:20]]) + "\n> ```\n")
            
            return "\n".join(snippets)
        except Exception as e:
            logging.error(f"Semantic search error: {e}")
            return ""

    def scan_workspace(self, query: str) -> str:
        """Searches the workspace using index, graph, and vector search."""
        if not self.index_file.exists():
            self.build_index()
        
        # Build vector index if it doesn't exist
        if HAS_CHROMADB and not self.db_path.exists():
            self.build_vector_index()
            
        try:
            with open(self.index_file, "r") as f:
                index = json.load(f)
        except Exception:
            index = {}

        root = self.file_path.parent
        context_snippets = []
        
        # 1. Check Graph & Symbols (Hybrid logic)
        # Check if query is a symbol in the graph
        impacted_files = self.graph_engine.get_impact_radius(query)
        if impacted_files:
            rel_files = ", ".join(list(impacted_files)[:5])
            context_snippets.append(f"> [!IMPORTANT] Graph analysis: '{query}' is a dependency for: {rel_files}\n")

        # 2. Check Memory (Lessons Learned)
        lessons = self.memory_engine.get_lessons_learned(query)
        if lessons:
            mem_blocks = []
            for l in lessons:
                status = "✅" if l["success"] else "❌"
                mem_blocks.append(f"> - {status} **{l['agent']}**: {l['task']} -> {l['outcome']}")
            context_snippets.append(f"> [!NOTE] Memory: Lessons from similar past tasks\n" + "\n".join(mem_blocks) + "\n")

        # 3. Check index first (Exact symbol/link matches)
        hits = index.get(query, [])
        for hit in hits:
            # Handle both string (legacy) and dict (new) formats from KnowledgeCore
            rel_path = hit["path"] if isinstance(hit, dict) else hit
            p = root / rel_path
            try:
                content = p.read_text(encoding="utf-8")
                lines = content.splitlines()
                # Find symbol definition specifically
                for i, line in enumerate(lines):
                    if f"def {query}" in line or f"class {query}" in line or query in line:
                        start = max(0, i - 5)
                        end = min(len(lines), i + 15)
                        snippet = "\n".join(lines[start:end])
                        context_snippets.append(f"> [!CODE] File: {rel_path} (from index)\n> ```python\n" + "\n".join([f"> {sl}" for sl in snippet.splitlines()]) + "\n> ```\n")
                        break
            except Exception:
                pass
            if len(context_snippets) > 5:
                break

        # 3. Semantic Search (ChromaDB)
        if HAS_CHROMADB:
            semantic_hits = self.semantic_search(query)
            if semantic_hits:
                context_snippets.append(semantic_hits)

        # 4. Fallback to grep-like scan if not enough hits
        if len(context_snippets) < 3:
            logging.info(f"Knowledge Agent fallback scan for: {query}")
            for p in root.rglob("*.py"):
                if any(part in str(p) for part in ["__pycache__", "venv", ".git"]) or str(p.relative_to(root)) in hits:
                    continue
                try:
                    content = p.read_text(encoding="utf-8")
                    if query.lower() in content.lower():
                        lines = content.splitlines()
                        for i, line in enumerate(lines):
                            if query.lower() in line.lower():
                                start = max(0, i - 5)
                                end = min(len(lines), i + 10)
                                snippet = "\n".join(lines[start:end])
                                context_snippets.append(f"> [!CODE] File: {p.relative_to(root)}\n> ```python\n" + "\n".join([f"> {sl}" for sl in snippet.splitlines()]) + "\n> ```\n")
                                break
                except Exception:
                    pass
                if len(context_snippets) > 10:
                    break
                
        if not context_snippets:
            return f"No relevant context found for '{query}' in {root}."
            
        return "## Gathered Context\n\n" + "\n".join(context_snippets)

    def find_backlinks(self, file_name: str) -> List[str]:
        """Finds all notes that link to the specified file/note name."""
        if not self.index_file.exists():
            self.build_index()
            
        try:
            with open(self.index_file, "r") as f:
                index = json.load(f)
        except Exception:
            index = {}
            
        # Strip extension for note name
        note_name = Path(file_name).stem
        return index.get(f"link:{note_name}", [])

    def auto_update_backlinks(self, directory: Optional[str] = None) -> int:
        """Updates all .md files in the directory with a Backlinks section."""
        root = Path(directory) if directory else self.file_path.parent
        if not root.is_dir():
            logging.error(f"Cannot update backlinks: {root} is not a directory")
            return 0
            
        updated_count = 0
        for p in root.rglob("*.md"):
            backlinks = self.find_backlinks(p.name)
            if not backlinks:
                continue
                
            try:
                content = p.read_text(encoding="utf-8")
                links_str = "\n".join([f"- [[{Path(b).stem}]]" for b in backlinks])
                backlink_section = f"\n\n## Backlinks\n\n{links_str}\n"
                
                if "## Backlinks" in content:
                    # Replace existing section
                    new_content = re.sub(r"## Backlinks\n.*?(?=\n\n##|\Z)", backlink_section.strip(), content, flags=re.DOTALL)
                else:
                    # Append to end
                    new_content = content.rstrip() + backlink_section
                
                if new_content != content:
                    p.write_text(new_content, encoding="utf-8")
                    updated_count += 1
                    logging.info(f"Updated backlinks for {p.name}")
            except Exception as e:
                logging.error(f"Failed to update backlinks for {p}: {e}")
                
        return updated_count

    def get_graph_mermaid(self) -> str:
        """Generates a Mermaid graph of the workspace note relationships."""
        if not self.index_file.exists():
            self.build_index()
            
        try:
            with open(self.index_file, "r") as f:
                index = json.load(f)
        except Exception:
            return "graph TD\n  Empty[No Index Found]"

        nodes = set()
        edges = []
        
        for key, paths in index.items():
            if key.startswith("link:"):
                target = key.replace("link:", "")
                nodes.add(target)
                for path in paths:
                    source = Path(path).stem
                    nodes.add(source)
                    edges.append(f"  {source} --> {target}")
        
        if not edges:
            return "graph TD\n  Start[No Links Detected]"
            
        return "graph TD\n" + "\n".join(edges)

    def get_compressed_briefing(self, file_paths: List[str]) -> str:
        """Generates a summarized structural briefing of multiple files."""
        root = self.file_path.parent
        summaries = []
        for path in file_paths:
            p = root / path
            if p.exists():
                summaries.append(self.compressor.compress_file(p))
        return "\n\n".join(summaries)

    def hybrid_search(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Combines semantic search with graph-based dependency analysis."""
        results = {
            "query": query,
            "semantic_matches": [],
            "related_nodes": [],
            "context_summary": ""
        }
        
        # 1. Semantic Search
        try:
            # We use MemoryEngine's chroma client or the internal one
            semantic_results = self.memory_engine.search_memories(query, limit=limit)
            results["semantic_matches"] = semantic_results
        except Exception as e:
            logging.error(f"Semantic search failed: {e}")

        # 2. Graph Expansion
        seen_nodes = set()
        for match in results["semantic_matches"]:
            match_text = match.get("content", "")
            symbols = re.findall(r"(?:class|def)\s+([a-zA-Z_][a-zA-Z0-9_]*)", match_text)
            
            for symbol in symbols:
                if symbol in seen_nodes:
                    continue
                seen_nodes.add(symbol)
                neighbors = self.graph_engine.get_neighbors(symbol)
                if neighbors:
                    results["related_nodes"].append({
                        "symbol": symbol,
                        "depends_on": neighbors.get("depends_on", []),
                        "depended_on_by": neighbors.get("depended_on_by", [])
                    })

        # 3. Contextual Compression
        files_to_compress = set()
        for match in results["semantic_matches"]:
            file_path = match.get("metadata", {}).get("file_path")
            if file_path:
                files_to_compress.add(file_path)
        
        if files_to_compress:
            compressed_bits = []
            for f in list(files_to_compress)[:3]:
                abs_f = Path(self.file_path.parent.parent.parent) / f
                if abs_f.exists():
                    compressed_bits.append(self.compressor.compress_file(str(abs_f)))
            results["context_summary"] = "\n\n".join(compressed_bits)

        return results

    @as_tool
    def query_knowledge(self, query: str) -> str:
        """User-facing knowledge query tool."""
        search_data = self.hybrid_search(query)
        
        report = [f"# Hybrid Search Results: '{query}'\n"]
        
        if search_data["semantic_matches"]:
            report.append("## 🔍 Semantic Matches")
            for m in search_data["semantic_matches"]:
                score = m.get("score", 0)
                path = m.get("metadata", {}).get("file_path", "unknown")
                report.append(f"- **{path}** (Score: {score:.4f})")
                
        if search_data["related_nodes"]:
            report.append("\n## 🕸️ Graph Relationships")
            for node in search_data["related_nodes"]:
                report.append(f"### {node['symbol']}")
                if node["depends_on"]:
                    report.append(f"- **Depends on**: {', '.join(node['depends_on'])}")
                if node["depended_on_by"]:
                    report.append(f"- **Depended on by**: {', '.join(node['depended_on_by'])}")
                    
        if search_data["context_summary"]:
            report.append("\n## 📄 Context Signatures")
            report.append(search_data["context_summary"])
            
        return "\n".join(report)

    def improve_content(self, prompt: str) -> str:
        """Override to provide contextual summary."""
        knowledge = self.query_knowledge(prompt)
        synthesis_prompt = (
            f"Synthesize the following codebase snippets into a briefing for another agent "
            f"regarding the topic: '{prompt}'\n\n{knowledge}"
        )
        return super().improve_content(synthesis_prompt)

if __name__ == "__main__":
    main = create_main_function(KnowledgeAgent, "Knowledge Agent", "Topic/Symbol to find context for")
    main()