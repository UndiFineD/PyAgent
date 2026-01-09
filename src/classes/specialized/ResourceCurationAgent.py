#!/usr/bin/env python3

"""ResourceCurationAgent for PyAgent.
Specializes in parsing, summarizing, and indexing external research links, 
blog posts, and technical papers into the agent's knowledge base.
"""

import logging
import json
import re
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

class ResourceCurationAgent(BaseAgent):
    """Manages the 'Good Read Unit' and research link lifecycle."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.library_path = "knowledge_exports/research_library.json"
        self._system_prompt = (
            "You are the Resource Curation Agent. Your goal is to keep the fleet's knowledge "
            "up-to-date by parsing research links, extracting actionable insights, and "
            "categorizing content for the KnowledgeAgent and FeatureStoreAgent."
        )

    @as_tool
    def add_resource(self, url: str, title: str, summary: Optional[str] = None, tags: List[str] = None) -> str:
        """Adds a new research resource to the library."""
        resource = {
            "url": url,
            "title": title,
            "summary": summary or "Pending automated summary",
            "tags": tags or [],
            "status": "Archived"
        }
        
        try:
            library = self._load_library()
            library.append(resource)
            self._save_library(library)
            return f"Resource '{title}' added to the Research Library."
        except Exception as e:
            return f"Failed to add resource: {e}"

    @as_tool
    def process_research_queue(self, urls: List[str]) -> str:
        """Bulk processes a list of discovery URLs."""
        # Simulated extraction logic
        return f"Processed {len(urls)} research items. Recommendations sent to KnowledgeAgent."

    def _load_library(self) -> List[Dict[str, Any]]:
        import os
        if not os.path.exists(self.library_path):
            return []
        with open(self.library_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_library(self, data: List[Dict[str, Any]]) -> None:
        with open(self.library_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def improve_content(self, input_text: str) -> str:
        return f"Library currently contains {len(self._load_library())} curated research units."

if __name__ == "__main__":
    from src.classes.base_agent.utilities import create_main_function
    main = create_main_function(ResourceCurationAgent, "Resource Curation Agent", "Curating research and documentation")
    main()
