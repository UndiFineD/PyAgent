#!/usr/bin/env python3

"""Agent specializing in consolidating episodic memories into global project context."""

from __future__ import annotations

import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.logic.agents.cognitive.context.engines.MemoryEngine import MemoryEngine
from src.logic.agents.cognitive.context.engines.GlobalContextEngine import GlobalContextEngine
from src.core.base.utilities import create_main_function, as_tool

class MemoryConsolidationAgent(BaseAgent):
    """Refines project knowledge by analyzing past interactions and outcomes."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self.memory_engine = MemoryEngine(str(self.workspace_root))
        self.context_engine = GlobalContextEngine(str(self.workspace_root))
        
        self._system_prompt = (
            "You are the Memory Consolidation Agent. "
            "Your task is to review episodic memories and extract long-term value. "
            "1. Identify repeating errors and turn them into constraints. "
            "2. Identify successful patterns and turn them into best practices (insights). "
            "3. Extract key architectural facts discovered during development."
        )

    def _get_default_content(self) -> str:
        return "# Memory Consolidation Log\n\n## Status\nReady for refinement.\n"

    @as_tool
    def consolidate_all(self) -> str:
        """Performs a full review of all recent memories."""
        episodes = self.memory_engine.episodes
        if not episodes:
            return "No episodic memories found to consolidate."
            
        new_facts = 0
        new_insights = 0
        
        # Heuristic approach for extraction (In reality, use LLM here)
        for ep in episodes:
            task = ep["task"].lower()
            outcome = ep["outcome"].lower()
            success = ep["success"]
            
            # Extract basic facts from task descriptions
            if "version" in task:
                self.context_engine.add_fact("project_version", ep["outcome"].split()[-1])
                new_facts += 1
                
            # Extract insights from failures
            if not success:
                if "import" in outcome or "module" in outcome:
                    self.context_engine.add_constraint("Always verify __init__.py exports before adding new sub-packages.")
                    new_insights += 1
                elif "pos" in outcome or "argument" in outcome:
                    self.context_engine.add_insight("Agent signatures are prone to drift. Verify base class inheritance.", "Consolidator")
                    new_insights += 1
            else:
                if "optimized" in task:
                    self.context_engine.add_insight(f"Successfully optimized: {task}", "Consolidator")
                    new_insights += 1
                    
        self.context_engine.save()
        report = f"✅ Consolidation complete. Extracted {new_facts} facts and {new_insights} insights/constraints."
        logging.info(report)
        return report

    def improve_content(self, prompt: str) -> str:
        """Trigger consolidation."""
        return self.consolidate_all()

if __name__ == "__main__":
    main = create_main_function(MemoryConsolidationAgent, "MemoryConsolidation Agent", "Consolidation Task")
    main()
