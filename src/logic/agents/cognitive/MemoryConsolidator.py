#!/usr/bin/env python3

"""Shell for MemoryConsolidator, handling storage and orchestration."""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.logic.cognitive.MemoryConsolidatorCore import MemoryConsolidatorCore

class MemoryConsolidator:
    """Manages the 'Sleep & Consolidate' phase for agents.
    
    Acts as the I/O Shell for MemoryConsolidatorCore.
    """

    def __init__(self, storage_path: str) -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.long_term_memory_file = self.storage_path / "long_term_memory.json"
        self.daily_buffer: List[Dict[str, Any]] = []
        self.core = MemoryConsolidatorCore()

    def record_interaction(self, agent: str, task: str, outcome: str) -> None:
        """Adds an interaction to the temporary daily buffer via Core."""
        entry = self.core.create_interaction_entry(agent, task, outcome)
        self.daily_buffer.append(entry)

    def sleep_and_consolidate(self) -> str:
        """Processes daily buffer into distilled long-term insights."""
        if not self.daily_buffer:
            return "No interactions to consolidate."
            
        logging.info("Entering sleep phase: Consolidating memories...")
        
        # Pure logic distillation
        consolidated_insights = self.core.distill_buffer(self.daily_buffer)
            
        # I/O: Append to long-term storage
        memory = self._load_memory()
        daily_record = self.core.format_daily_memory(consolidated_insights)
        memory.append(daily_record)
        
        self._save_memory(memory)
        
        total_interactions = len(self.daily_buffer)
        self.daily_buffer = [] # Clear buffer
        return f"Consolidated {total_interactions} interactions into {len(consolidated_insights)} insights."

    def _load_memory(self) -> List[Dict[str, Any]]:
        """I/O: Load memory from disk."""
        if self.long_term_memory_file.exists():
            try:
                with open(self.long_term_memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to load memory: {e}")
        return []

    def _save_memory(self, memory: List[Dict[str, Any]]) -> None:
        """I/O: Save memory to disk."""
        try:
            with open(self.long_term_memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save memory: {e}")
            
    def query_long_term_memory(self, query: str) -> List[str]:
        """I/O and Core combined search."""
        memory = self._load_memory()
        return self.core.filter_memory_by_query(memory, query)
