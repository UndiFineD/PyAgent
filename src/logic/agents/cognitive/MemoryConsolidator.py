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

"""Shell for MemoryConsolidator, handling storage and orchestration."""

from __future__ import annotations
from src.core.base.version import VERSION
import json
import logging
from pathlib import Path
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
# Fixed import path assuming Core is in the same directory
from src.logic.agents.cognitive.MemoryConsolidatorCore import MemoryConsolidatorCore

__version__ = VERSION




class MemoryConsolidator(BaseAgent):
    """Manages the 'Sleep & Consolidate' phase for agents.

    Acts as the I/O Shell for MemoryConsolidatorCore.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        # Use workspace root from BaseAgent if available, or derive from file_path
        self.storage_path = Path("data/memory")  # Default path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.long_term_memory_file = self.storage_path / "long_term_memory.json"
        self.daily_buffer: list[dict[str, Any]] = []
        self.core = MemoryConsolidatorCore()

    @as_tool
    def record_interaction(self, agent: str, task: str, outcome: str) -> None:
        """Adds an interaction to the temporary daily buffer via Core."""
        entry = self.core.create_interaction_entry(agent, task, outcome)
        self.daily_buffer.append(entry)

    @as_tool
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
        self.daily_buffer = []  # Clear buffer
        return f"Consolidated {total_interactions} interactions into {len(consolidated_insights)} insights."

    def _load_memory(self) -> list[dict[str, Any]]:
        """I/O: Load memory from disk."""
        if self.long_term_memory_file.exists():
            try:
                with open(self.long_term_memory_file, encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to load memory: {e}")
        return []

    def _save_memory(self, memory: list[dict[str, Any]]) -> None:
        """I/O: Save memory to disk atomically."""
        temp_path = self.long_term_memory_file.with_suffix(".tmp")
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(memory, f, indent=2)
            temp_path.replace(self.long_term_memory_file)
        except Exception as e:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass
            logging.error(f"Failed to save memory atomically: {e}")
            raise

    @as_tool
    def query_long_term_memory(self, query: str) -> list[str]:
        """I/O and Core combined search."""
        memory = self._load_memory()
        return self.core.filter_memory_by_query(memory, query)
