#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/mixins/ContextConsolidationMixin.description.md

# ContextConsolidationMixin

**File**: `src\logic\agents\cognitive\context\engines\mixins\ContextConsolidationMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 54  
**Complexity**: 2 (simple)

## Overview

Consolidation and summary logic for GlobalContextEngine.

## Classes (1)

### `ContextConsolidationMixin`

Mixin for summarizing memory and consolidating episodes.

**Methods** (2):
- `get_summary(self)`
- `consolidate_episodes(self, episodes)`

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/mixins/ContextConsolidationMixin.improvements.md

# Improvements for ContextConsolidationMixin

**File**: `src\logic\agents\cognitive\context\engines\mixins\ContextConsolidationMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 54 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextConsolidationMixin_test.py` with pytest tests

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

"""Consolidation and summary logic for GlobalContextEngine."""

from typing import Any

class ContextConsolidationMixin:
    """Mixin for summarizing memory and consolidating episodes."""

    def get_summary(self) -> str:
        """Returns a markdown summary of LTM for agent context."""
        if hasattr(self, "core") and hasattr(self, "memory"):
            return self.core.generate_markdown_summary(self.memory)
        return ""

    def consolidate_episodes(self, episodes: list[dict[str, Any]]) -> None:
        """Analyzes episodic memories to extract long-term insights."""
        # This would typically use an LLM to find patterns.
        # For now, we look for repeated failures or success patterns.
        agent_stats: dict[str, dict[str, int]] = {}
        for ep in episodes:
            agent = ep["agent"]
            if agent not in agent_stats:
                agent_stats[agent] = {"success": 0, "fail": 0}
            if ep["success"]:
                agent_stats[agent]["success"] += 1
            else:
                agent_stats[agent]["fail"] += 1

        for agent, stats in agent_stats.items():
            if stats["fail"] > 3:
                if hasattr(self, "add_insight"):
                    self.add_insight(
                        f"{agent} is struggling with current tasks. Context injection might be insufficient.",
                        "LTM_System",
                    )
            elif stats["success"] > 10:
                if hasattr(self, "add_insight"):
                    self.add_insight(
                        f"{agent} is highly reliable for current task types.", "LTM_System"
                    )
