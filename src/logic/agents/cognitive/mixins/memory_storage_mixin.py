# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import json
import time
import logging
from typing import TYPE_CHECKING
from src.core.base.common.base_utilities import as_tool

if TYPE_CHECKING:
    from src.logic.agents.cognitive.hierarchical_memory_agent import HierarchicalMemoryAgent

class MemoryStorageMixin:
    """Mixin for memory storage and promotion in HierarchicalMemoryAgent."""

    @as_tool
    def store_memory(
        self: HierarchicalMemoryAgent, content: str, importance: float = 0.5, tags: list[str] | None = None
    ) -> str:
        """Stores a new memory fragment into the ShortTerm tier."""
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
    def promote_memories(self: HierarchicalMemoryAgent) -> str:
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
