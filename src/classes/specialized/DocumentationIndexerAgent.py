#!/usr/bin/env python3

"""Agent specializing in workspace-wide documentation indexing and retrieval (Tabby pattern)."""

from src.classes.base_agent import BaseAgent
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

class DocumentationIndexerAgent(BaseAgent):
    """Indexes workspace documentation and provides structured navigation/search."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Documentation Indexer Agent. "
            "Your role is to crawl the workspace, build a map of all documentation, "
            "and provide semantic pointers to relevant sections when asked."
        )

    def build_index(self, root_path: str) -> Dict[str, List[str]]:
        """Crawls the workspace for markdown and text documentation."""
        index = {"docs": [], "source_comments": [], "readmes": []}
        root = Path(root_path)
        
        for p in root.rglob("*.md"):
            if "README" in p.name:
                index["readmes"].append(str(p.relative_to(root)))
            else:
                index["docs"].append(str(p.relative_to(root)))
                
        for p in root.rglob("*.py"):
            # Potential for extracting docstrings
            pass
            
        return index

    def get_semantic_pointers(self, query: str) -> str:
        """Returns pointers to documentation relevant to the query."""
        # This would use semantic search in a real implementation
        return f"Searching index for: {query}... (Pointers to be generated via embeddings)"

    def improve_content(self, input_text: str) -> str:
        """Returns documentation snippets or paths."""
        return self.get_semantic_pointers(input_text)

if __name__ == "__main__":
    from src.classes.base_agent.utilities import create_main_function
    main = create_main_function(DocumentationIndexerAgent, "Documentation Indexer Agent", "Path to index")
    main()
