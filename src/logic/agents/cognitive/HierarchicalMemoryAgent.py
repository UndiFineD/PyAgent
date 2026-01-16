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

"""Agent specializing in Multi-Resolution Hierarchical Memory.
Manages Short-term (Episodic), Mid-term (Working), Long-term (Semantic), and Archival storage tiers.
"""

from __future__ import annotations
from src.core.base.Version import VERSION
import json
import time
from pathlib import Path
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool

__version__ = VERSION


class HierarchicalMemoryAgent(BaseAgent):
    """Manages memory across multiple temporal and semantic resolutions.
    Phase 290: Integrated with 3-layer system (ShortTerm, Working, LongTerm).
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.memory_root = Path("data/logs/memory_hierarchical")
        # Phase 290: Standardized 3-layer tiers + Archival
        self.tiers = ["ShortTerm", "Working", "LongTerm", "Archival"]
        for tier in self.tiers:
            (self.memory_root / tier).mkdir(parents=True, exist_ok=True)

        self._system_prompt = (
            "You are the Hierarchical Memory Agent. "
            "Your role is to categorize and move information between different memory tiers. "
            "ShortTerm memory: Recent raw telemetry and episodic events. "
            "Working memory: Task-specific context and scratchpad data. "
            "LongTerm memory: Distilled semantic knowledge and reusable patterns. "
            "Archival memory: Highly compressed historical logs for auditing."
        )

    @as_tool
    def store_memory(
        self, content: str, importance: float = 0.5, tags: list[str] | None = None
    ) -> str:
        """Stores a new memory fragment into the ShortTerm tier.
        Args:
            content: The actual memory text.
            importance: 0.0 to 1.0 score. High importance may bypass Working tier.
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
            "status": "ShortTerm",
        }

        target_path = self.memory_root / "ShortTerm" / f"{memory_id}.json"
        with open(target_path, "w") as f_out:
            json.dump(data, f_out, indent=2)

        return f"Memory {memory_id} stored in ShortTerm tier."

    @as_tool
    def promote_memories(self) -> str:
        """Analyzes ShortTerm and Working memories to move them to higher tiers."""
        promoted_count = 0
        current_time = time.time()

        # 1. Promote from ShortTerm to Working or LongTerm
        short_dir = self.memory_root / "ShortTerm"
        for mem_file in short_dir.glob("*.json"):
            try:
                with open(mem_file) as f_in:
                    data = json.load(f_in)

                if current_time - data["timestamp"] > 3600 or data["importance"] > 0.8:
                    tier = "LongTerm" if data["importance"] > 0.9 else "Working"
                    data["status"] = tier

                    new_path = self.memory_root / tier / mem_file.name
                    with open(new_path, "w") as f_out:
                        json.dump(data, f_out, indent=2)
                    mem_file.unlink()
                    promoted_count += 1
            except Exception as e:
                logging.error(f"Failed to promote {mem_file}: {e}")

        return f"Consolidation complete. Promoted {promoted_count} memory fragments."

    @as_tool
    def hierarchical_query(self, query: str, deep_search: bool = False) -> str:
        """Searches across memory tiers starting from short-term.
        Args:
            query: The search term or semantic query.
            deep_search: If True, searches long-term and archival tiers.
        """
        search_tiers = ["short", "mid"]
        if deep_search:
            search_tiers += ["long", "archival"]

        # Collect all memory files
        all_data = []  # (tier, content, tags)
        for tier in search_tiers:
            tier_dir = self.memory_root / tier
            for mem_file in tier_dir.glob("*.json"):
                try:
                    with open(mem_file) as f:
                        data = json.load(f)
                    all_data.append((tier, data.get("content", ""), data.get("tags", [])))
                except Exception:
                    continue
        
        if not all_data:
            return "No matching memories found."
        
        # Rust-accelerated search
        try:
            from rust_core import search_with_tags_rust
            contents = [d[1] for d in all_data]
            tags_list = [d[2] for d in all_data]
            matches = search_with_tags_rust(query, contents, tags_list)
            
            results = []
            for idx, score in matches:
                tier, content, _ = all_data[idx]
                results.append(f"[{tier.upper()}] {content[:100]}...")
            
            if not results:
                return "No matching memories found."
            return "### Memory Search Results\n\n" + "\n".join(results)
        except (ImportError, Exception):
            pass  # Fall back to Python
        
        # Python fallback
        results = []
        for tier, content, tags in all_data:
            if query.lower() in content.lower() or any(
                query.lower() in t.lower() for t in tags
            ):
                results.append(f"[{tier.upper()}] {content[:100]}...")

        if not results:
            return "No matching memories found."

        return "### Memory Search Results\n\n" + "\n".join(results)

    def improve_content(self, prompt: str) -> str:
        return "Hierarchical memory is synchronized and optimized."


if __name__ == "__main__":
    from src.core.base.BaseUtilities import create_main_function

    main = create_main_function(
        HierarchicalMemoryAgent,
        "Hierarchical Memory Agent",
        "Multi-resolution memory management",
    )
    main()
