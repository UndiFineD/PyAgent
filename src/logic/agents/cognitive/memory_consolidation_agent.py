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

"""Agent specializing in consolidating episodic memories into global project context."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import Dict
from src.core.base.BaseAgent import BaseAgent
from src.logic.agents.cognitive.LongTermMemory import LongTermMemory
from src.logic.agents.cognitive.context.engines.GlobalContextEngine import GlobalContextEngine
from src.core.base.utilities import create_main_function, as_tool

__version__ = VERSION

class MemoryConsolidationAgent(BaseAgent):
    """Refines project knowledge by analyzing past interactions and outcomes from federated shards."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self.ltm = LongTermMemory(agent_name="consolidator")
        self.context_engine = GlobalContextEngine(str(self.workspace_root))
        
        self._system_prompt = (
            "You are the Memory Consolidation Agent. "
            "Your task is to review federated DiskCache memory shards and extract long-term value. "
            "1. Merge duplicate interactions into high-level factual summaries. "
            "2. Identify successful patterns and turn them into best practices. "
            "3. Prune redundant episodic data from local shards."
        )

    def _get_default_content(self) -> str:
        return "# Memory Consolidation Log\n\n## Status\nReady for federated consolidation.\n"

    @as_tool
    def consolidate_all(self) -> str:
        """Performs a full review of all federated memory shards."""
        # Querying for common themes across federation
        recent_memories = self.ltm.federated_query("", n_results=100) # Empty query to get general recent ones
        if not recent_memories:
            return "No memories found in federated shards to consolidate."
            
        new_facts = 0
        new_insights = 0
        deduplicated = 0
        
        seen_texts: Dict[str, str] = {}
        
        for mem in recent_memories:
            content = mem["content"]
            meta = mem.get("metadata", {})
            
            # Simple deduplication logic
            content_hash = hash(content)
            if content_hash in seen_texts:
                deduplicated += 1
                continue
            seen_texts[content_hash] = content
            
            task = content.lower()
            
            # Extraction logic (Enhanced for Phase 151)
            if "version" in task:
                version_val = content.split()[-1]
                self.context_engine.add_fact("project_version_recorded", version_val)
                new_facts += 1
            
            if "error" in task or "failed" in task:
                if "import" in task:
                    self.context_engine.add_constraint("Verify __init__.py exports for all RAG shards.")
                    new_insights += 1
                elif "diskcache" in task:
                    self.context_engine.add_insight("DiskCache performance hinges on shard size. Keep shards < 1GB.", "Consolidator")
                    new_insights += 1
            
        self.context_engine.save()
        report = f"✅ Consolidation complete. Shards scanned. Extracted {new_facts} facts, {new_insights} insights. Deduplicated {deduplicated} items."
        logging.info(report)
        return report

    def improve_content(self, prompt: str) -> str:
        """Trigger consolidation cycle."""
        return self.consolidate_all()

if __name__ == "__main__":
    main = create_main_function(MemoryConsolidationAgent, "MemoryConsolidation Agent", "Consolidation Task")
    main()