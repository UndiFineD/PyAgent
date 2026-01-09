#!/usr/bin/env python3

"""Memory consolidation engine for long-term agent retention.
Summarizes daily logs into distilled 'insights' for long-term memory.
"""

import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Any

class MemoryConsolidator:
    """Manages the 'Sleep & Consolidate' phase for agents."""

    def __init__(self, storage_path: str) -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.long_term_memory_file = self.storage_path / "long_term_memory.json"
        self.daily_buffer: List[Dict[str, Any]] = []

    def record_interaction(self, agent: str, task: str, outcome: str) -> str:
        """Adds an interaction to the temporary daily buffer."""
        self.daily_buffer.append({
            "timestamp": time.time(),
            "agent": agent,
            "task": task,
            "outcome": outcome
        })

    def sleep_and_consolidate(self) -> str:
        """Processes daily buffer into distilled long-term insights."""
        if not self.daily_buffer:
            return "No interactions to consolidate."
            
        logging.info("Entering sleep phase: Consolidating memories...")
        
        # Simulate distillation logic (e.g. LLM summarization)
        # Group by agent
        summary = {}
        for entry in self.daily_buffer:
            agent = entry["agent"]
            if agent not in summary:
                summary[agent] = []
            summary[agent].append(entry["task"])
            
        consolidated = []
        for agent, tasks in summary.items():
            insight = f"{agent} completed {len(tasks)} tasks today. Key focus: {tasks[-1]}."
            consolidated.append(insight)
            
        # Append to long-term storage
        memory = self._load_memory()
        memory.append({
            "date": time.strftime("%Y-%m-%d"),
            "insights": consolidated
        })
        self._save_memory(memory)
        
        count = len(self.daily_buffer)
        self.daily_buffer = [] # Clear buffer
        return f"Consolidated {count} interactions into {len(consolidated)} long-term insights."

    def _load_memory(self) -> List[Dict[str, Any]]:
        if self.long_term_memory_file.exists():
            with open(self.long_term_memory_file, 'r') as f:
                return json.load(f)
        return []

    def _save_memory(self, memory: List[Dict[str, Any]]):
        with open(self.long_term_memory_file, 'w') as f:
            json.dump(memory, f, indent=2)
            
    def query_long_term_memory(self, query: str) -> List[str]:
        """Simple keyword search across consolidated insights."""
        memory = self._load_memory()
        matches = []
        for day in memory:
            for insight in day["insights"]:
                if query.lower() in insight.lower():
                    matches.append(f"{day['date']}: {insight}")
        return matches
