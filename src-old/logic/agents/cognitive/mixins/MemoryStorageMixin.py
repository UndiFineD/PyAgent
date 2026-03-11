"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/mixins/MemoryStorageMixin.description.md

# MemoryStorageMixin

**File**: `src\\logic\agents\\cognitive\\mixins\\MemoryStorageMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 64  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for MemoryStorageMixin.

## Classes (1)

### `MemoryStorageMixin`

Mixin for memory storage and promotion in HierarchicalMemoryAgent.

**Methods** (2):
- `store_memory(self, content, importance, tags)`
- `promote_memories(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `json`
- `logging`
- `src.core.base.BaseUtilities.as_tool`
- `src.logic.agents.cognitive.HierarchicalMemoryAgent.HierarchicalMemoryAgent`
- `time`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/mixins/MemoryStorageMixin.improvements.md

# Improvements for MemoryStorageMixin

**File**: `src\\logic\agents\\cognitive\\mixins\\MemoryStorageMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 64 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MemoryStorageMixin_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
import json
import logging
import time

from src.core.base.BaseUtilities import as_tool
from src.logic.agents.cognitive.HierarchicalMemoryAgent import HierarchicalMemoryAgent


class MemoryStorageMixin:
    """Mixin for memory storage and promotion in HierarchicalMemoryAgent."""

    @as_tool
    def store_memory(
        self: HierarchicalMemoryAgent,
        content: str,
        importance: float = 0.5,
        tags: list[str] | None = None,
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
