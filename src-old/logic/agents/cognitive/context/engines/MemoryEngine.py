#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/MemoryEngine.description.md

# MemoryEngine

**File**: `src\logic\agents\cognitive\context\engines\MemoryEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 40  
**Complexity**: 1 (simple)

## Overview

Engine for persistent episodic memory of agent actions and outcomes.

## Classes (1)

### `MemoryEngine`

**Inherits from**: MemoryStorageMixin, MemoryEpisodeMixin, MemorySearchMixin

Stores and retrieves historical agent contexts and lessons learned.

**Methods** (1):
- `__init__(self, workspace_root)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `memory_mixins.MemoryEpisodeMixin.MemoryEpisodeMixin`
- `memory_mixins.MemorySearchMixin.MemorySearchMixin`
- `memory_mixins.MemoryStorageMixin.MemoryStorageMixin`
- `pathlib.Path`
- `src.core.base.Version.VERSION`
- `src.logic.agents.cognitive.context.engines.MemoryCore.MemoryCore`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/MemoryEngine.improvements.md

# Improvements for MemoryEngine

**File**: `src\logic\agents\cognitive\context\engines\MemoryEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 40 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MemoryEngine_test.py` with pytest tests

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


"""Engine for persistent episodic memory of agent actions and outcomes."""

from src.core.base.Version import VERSION
from pathlib import Path
from typing import Any
from src.logic.agents.cognitive.context.engines.MemoryCore import MemoryCore
from .memory_mixins.MemoryStorageMixin import MemoryStorageMixin
from .memory_mixins.MemoryEpisodeMixin import MemoryEpisodeMixin
from .memory_mixins.MemorySearchMixin import MemorySearchMixin

__version__ = VERSION


class MemoryEngine(MemoryStorageMixin, MemoryEpisodeMixin, MemorySearchMixin):
    """Stores and retrieves historical agent contexts and lessons learned."""

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.memory_file = self.workspace_root / ".agent_memory.json"
        self.db_path = self.workspace_root / "data/db/.agent_memory_db"
        self.episodes: list[dict[str, Any]] = []
        self._collection = None
        self.core = MemoryCore()
        self.load()
