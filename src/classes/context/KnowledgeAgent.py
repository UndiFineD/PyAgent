#!/usr/bin/env python3

"""Agent specializing in Workspace Knowledge and Codebase Context (RAG-lite)."""

from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function
import logging
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False

class KnowledgeAgent(BaseAgent):
    """Agent that scans the workspace to provide deep context to other agents."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.index_file = self.file_path.parent / ".agent_knowledge_index.json"
        self.db_path = self.file_path.parent / ".agent_chroma_db"
        self._chroma_client = None
        self._collection = None
        
        self._system_prompt = (
            "You are the Knowledge Agent (RAG Specialist). "
            "Your role is to understand the codebase structure and logic. "
            "You scan files, find definitions, and explain dependencies. "
            "Provide detailed summaries of how different modules interact. "
            "Format your findings using Obsidian-style callouts for clarity (e.g., > [!CODE] for snippets, > [!INFO] for architecture)."
        )

    def _get_default_content(self) -> str:
        return "# Workspace Knowledge Map\n\n## Summary\nPending scan...\n"

    def build_index(self):
        """Builds a simple keyword/symbol index of the workspace."""
        root = self.file_path.parent
        index = {}
        
        # Scan Python and Markdown files
        for p in root.rglob("*"):
            if p.is_dir() or p.suffix not in [".py", ".md"]:
                continue
            if any(part in str(p) for part in ["__pycache__", "venv", ".git"]):
                continue
            try:
                content = p.read_text(encoding="utf-8")
                
                if p.suffix == ".py":
                    # Simple symbol extraction (def/class)
                    symbols = re.findall(r"(?:def|class)\s+([a-zA-Z_][a-zA-Z0-9_]*)", content)
                    for sym in symbols:
                        if sym not in index:
                            index[sym] = []
                        index[sym].append(str(p.relative_to(root)))
                
                # Index Obsidian Wikilinks (primarily in .md files)
                if p.suffix == ".md":
                    # Matches [[Target]] or [[Target|Display Name]]
                    links = re.findall(r"\[\[([^\[\]|#]+)(?:[|#][^\]]*)?\]\]", content)
                    for link in links:
                        link = link.strip()
                        link_key = f"link:{link}"
                        if link_key not in index:
                            index[link_key] = []
                        # Avoid duplicates
                        rel_path = str(p.relative_to(root))
                        if rel_path not in index[link_key]:
                            index[link_key].append(rel_path)

            except Exception as e:
                logging.error(f"Index error for {p}: {e}")
                
        with open(self.index_file, "w") as f:
            json.dump(index, f, indent=4)
        logging.info(f"Knowledge index built with {len(index)} symbols.")

    def _init_chroma(self):
        """Initialize ChromaDB client and collection."""
        if not HAS_CHROMADB:
            return False
        
        try:
            if self._chroma_client is None:
                self._chroma_client = chromadb.PersistentClient(path=str(self.db_path))
                self._collection = self._chroma_client.get_or_create_collection(name="workspace_docs")
            return True
        except Exception as e:
            logging.error(f"ChromaDB init error: {e}")
            return False

    def build_vector_index(self):
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
            if any(part in str(p) for part in ["__pycache__", "venv", ".git", ".agent_chroma_db"]):
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
        """Searches the workspace using index first, then vector search, then fallback to scan."""
        if not self.index_file.exists():
            self.build_index()
        
        # Build vector index if it doesn't exist
        if HAS_CHROMADB and not self.db_path.exists():
            self.build_vector_index()
            
        try:
            with open(self.index_file, "r") as f:
                index = json.load(f)
        except:
            index = {}

        root = self.file_path.parent
        context_snippets = []
        
        # 1. Check index first (Exact symbol/link matches)
        hits = index.get(query, [])
        for rel_path in hits:
            p = root / rel_path
            try:
                content = p.read_text(encoding="utf-8")
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if query in line:
                        start = max(0, i - 5)
                        end = min(len(lines), i + 15)
                        snippet = "\n".join(lines[start:end])
                        context_snippets.append(f"> [!CODE] File: {rel_path} (from index)\n> ```python\n" + "\n".join([f"> {sl}" for sl in snippet.splitlines()]) + "\n> ```\n")
                        break
            except:
                pass
            if len(context_snippets) > 3: break

        # 2. Semantic Search (ChromaDB)
        if HAS_CHROMADB:
            semantic_hits = self.semantic_search(query)
            if semantic_hits:
                context_snippets.append(semantic_hits)

        # 3. Fallback to grep-like scan if not enough hits
        if len(context_snippets) < 2:
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
                except:
                    pass
                if len(context_snippets) > 8: break
                
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
        except:
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
        except:
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

    def improve_content(self, prompt: str) -> str:
        """Override to provide contextual summary."""
        knowledge = self.scan_workspace(prompt)
        synthesis_prompt = (
            f"Synthesize the following codebase snippets into a briefing for another agent "
            f"regarding the topic: '{prompt}'\n\n{knowledge}"
        )
        return super().improve_content(synthesis_prompt)

if __name__ == "__main__":
    main = create_main_function(KnowledgeAgent, "Knowledge Agent", "Topic/Symbol to find context for")
    main()
