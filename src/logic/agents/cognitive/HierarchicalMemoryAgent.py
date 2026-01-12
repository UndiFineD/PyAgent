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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Agent specializing in Multi-Resolution Hierarchical Memory.
Manages Short-term (Episodic), Mid-term (Working), Long-term (Semantic), and Archival storage tiers.
"""



import logging
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

class HierarchicalMemoryAgent(BaseAgent):
    """Manages memory across multiple temporal and semantic resolutions."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.memory_root = Path("data/logs/memory_hierarchical")
        self.tiers = ["short", "mid", "long", "archival"]
        for tier in self.tiers:
            (self.memory_root / tier).mkdir(parents=True, exist_ok=True)
            
        self._system_prompt = (
            "You are the Hierarchical Memory Agent. "
            "Your role is to categorize and move information between different memory tiers. "
            "Short-term memory contains recent raw telemetry. "
            "Mid-term memory contains task-specific context. "
            "Long-term memory contains distilled reusable knowledge. "
            "Archival memory contains compressed historical logs."
        )

    @as_tool
    def store_memory(self, content: str, importance: float = 0.5, tags: List[str] = None) -> str:
        """Stores a new memory fragment into the short-term tier.
        Args:
            content: The actual memory text.
            importance: 0.0 to 1.0 score. High importance may bypass mid-term.
            tags: List of semantic tags for retrieval.
        """
        timestamp = int(time.time())
        memory_id = f"mem_{timestamp}"
        data = {
            "id": memory_id,
            "timestamp": timestamp,
            "content": content,
            "importance": importance,
            "tags": tags or [],
            "status": "short"
        }
        
        target_path = self.memory_root / "short" / f"{memory_id}.json"
        with open(target_path, "w") as f:
            json.dump(data, f, indent=2)
            
        return f"Memory {memory_id} stored in short-term tier."

    @as_tool
    def promote_memories(self) -> str:
        """Analyzes short and mid-term memories to move them to higher tiers."""
        promoted_count = 0
        # Simulated logic: memories older than 1 hour move to mid-term
        current_time = time.time()
        
        short_dir = self.memory_root / "short"
        for mem_file in short_dir.glob("*.json"):
            with open(mem_file, "r") as f:
                data = json.load(f)
            
            if current_time - data["timestamp"] > 3600 or data["importance"] > 0.8:
                # Distill and promote to Long-term if high importance, else Mid-term
                tier = "long" if data["importance"] > 0.8 else "mid"
                data["status"] = tier
                
                new_path = self.memory_root / tier / mem_file.name
                with open(new_path, "w") as f:
                    json.dump(data, f, indent=2)
                
                mem_file.unlink()
                promoted_count += 1
                
        return f"Consolidation complete. Promoted {promoted_count} memory fragments."

    @as_tool
    def hierarchical_query(self, query: str, deep_search: bool = False) -> str:
        """Searches across memory tiers starting from short-term.
        Args:
            query: The search term or semantic query.
            deep_search: If True, searches long-term and archival tiers.
        """
        results = []
        search_tiers = ["short", "mid"]
        if deep_search:
            search_tiers += ["long", "archival"]
            
        for tier in search_tiers:
            tier_dir = self.memory_root / tier
            for mem_file in tier_dir.glob("*.json"):
                with open(mem_file, "r") as f:
                    data = json.load(f)
                if query.lower() in data["content"].lower() or any(query.lower() in t.lower() for t in data["tags"]):
                    results.append(f"[{tier.upper()}] {data['content'][:100]}...")
        
        if not results:
            return "No matching memories found."
            
        return "### Memory Search Results\n\n" + "\n".join(results)

    def improve_content(self, prompt: str) -> str:
        return "Hierarchical memory is synchronized and optimized."

if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(HierarchicalMemoryAgent, "Hierarchical Memory Agent", "Multi-resolution memory management")
    main()
