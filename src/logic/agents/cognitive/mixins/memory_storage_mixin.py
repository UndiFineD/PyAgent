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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.



"""
MemoryStorageMixin: Provides hierarchical memory storage and promotion logic for Memory Agents in PyAgent.
Handles memory persistence, promotion, and distributed storage strategies.
Provides the machinery for persisting memory fragments into tiers and promoting them based on importance, recency, and utility metrics.
"""

from __future__ import annotations
import json
import logging
import time
from typing import TYPE_CHECKING
from src.core.base.lifecycle.version import VERSION
from src.core.base.common.base_utilities import as_tool

if TYPE_CHECKING:
    from src.logic.agents.cognitive.hierarchical_memory_agent import HierarchicalMemoryAgent

__version__ = VERSION


class MemoryStorageMixin:
    """Mixin for memory storage and promotion in HierarchicalMemoryAgent."""

    @as_tool
    def store_memory(
        self: HierarchicalMemoryAgent,
        content: str,
        importance: float = 0.5,
        tags: list[str] | None = None,
    ) -> str:
        """Stores a new memory fragment into the ShortTerm tier.

        Args:
            content: The text content of the memory.
            importance: Floating point importance score (0.0 to 1.0).
            tags: Optional list of categorical tags.

        Returns:
            Success message with the memory ID.
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

        target_dir = self.memory_root / "ShortTerm"
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / f"{memory_id}.json"

        with open(target_path, "w", encoding="utf-8") as f_out:
            json.dump(data, f_out, indent=2)

        return f"Memory {memory_id} stored in ShortTerm tier."

    @as_tool
    def promote_memories(self: HierarchicalMemoryAgent) -> str:
        """Analyzes ShortTerm and Working memories to move them to higher tiers.

        Returns:
            Summary of promoted memory counts.
        """
        promoted_count = 0
        current_time = time.time()

        # 1. Promote from ShortTerm to Working or LongTerm
        short_dir = self.memory_root / "ShortTerm"
        if not short_dir.exists():
            return "Consolidation complete. 0 fragments promoted."

        for mem_file in short_dir.glob("*.json"):
            try:
                with open(mem_file, encoding="utf-8") as f_in:
                    data = json.load(f_in)

                if current_time - data["timestamp"] > 3600 or data["importance"] > 0.8:
                    tier = "LongTerm" if data["importance"] > 0.9 else "Working"
                    data["status"] = tier

                    new_dir = self.memory_root / tier
                    new_dir.mkdir(parents=True, exist_ok=True)
                    new_path = new_dir / mem_file.name

                    with open(new_path, "w", encoding="utf-8") as f_out:
                        json.dump(data, f_out, indent=2)
                    mem_file.unlink()
                    promoted_count += 1
            except (json.JSONDecodeError, OSError) as e:
                logging.error(f"Failed to promote {mem_file}: {e}")

        return f"Consolidation complete. Promoted {promoted_count} memory fragments."
