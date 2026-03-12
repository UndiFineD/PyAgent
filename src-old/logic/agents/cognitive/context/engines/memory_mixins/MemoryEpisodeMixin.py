# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/memory_mixins/MemoryEpisodeMixin.description.md

# MemoryEpisodeMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\memory_mixins\\MemoryEpisodeMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 67  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for MemoryEpisodeMixin.

## Classes (1)

### `MemoryEpisodeMixin`

Methods for recording and updating episodes.

**Methods** (2):
- `record_episode(self, agent_name, task, outcome, success, metadata)`
- `update_utility(self, memory_id, increment)`

## Dependencies

**Imports** (3):
- `datetime.datetime`
- `logging`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/memory_mixins/MemoryEpisodeMixin.improvements.md

# Improvements for MemoryEpisodeMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\memory_mixins\\MemoryEpisodeMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 67 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MemoryEpisodeMixin_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import logging
from datetime import datetime
from typing import Any


class MemoryEpisodeMixin:
    """Methods for recording and updating episodes."""

    def record_episode(
        self,
        agent_name: str,
        task: str,
        outcome: str,
        success: bool,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Records an agent's experience with semantic indexing and utility scoring."""
        episode = self.core.create_episode(agent_name, task, outcome, success, metadata)
        self.episodes.append(episode)

        # Add to vector db for semantic recall
        collection = self._init_db()
        if collection:
            try:
                doc = self.core.format_for_indexing(episode)
                collection.add(
                    documents=[doc],
                    metadatas=[
                        {
                            "agent": episode["agent"],
                            "success": str(episode["success"]),
                            "timestamp": episode["timestamp"],
                            "utility_score": float(episode["utility_score"]),
                        }
                    ],
                    ids=[f"mem_{len(self.episodes)}_{int(datetime.now().timestamp())}"],
                )
            except Exception as e:
                logging.error(f"Failed to index memory: {e}")

        self.save()

    def update_utility(self, memory_id: str, increment: float) -> None:
        """Updates the utility score of a specific memory episode."""
        collection = self._init_db()
        if not collection:
            return

        try:
            # Fetch existing metadata
            result = collection.get(ids=[memory_id])
            if result and result["metadatas"]:
                meta = result["metadatas"][0]
                old_score = float(meta.get("utility_score", 0.5))
                new_score = self.core.calculate_new_utility(old_score, increment)
                meta["utility_score"] = new_score

                collection.update(ids=[memory_id], metadatas=[meta])

                # Update local list too
                for ep in self.episodes:
                    # Note: memory_id format check or matching logic here
                    pass
        except Exception as e:
            logging.error(f"Failed to update utility for {memory_id}: {e}")
