#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/GlobalContextEngine.description.md

# GlobalContextEngine

**File**: `src\classes\context\GlobalContextEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 64  
**Complexity**: 1 (simple)

## Overview

Advanced Long-Term Memory (LTM) for agents.
Consolidates episodic memories into semantic knowledge and persistent preferences.
Inspired by mem0 and BabyAGI patterns.

## Classes (1)

### `GlobalContextEngine`

**Inherits from**: ContextShardMixin, ContextDataMixin, ContextEntityMixin, ContextConsolidationMixin

Manages persistent project-wide knowledge and agent preferences.
Shell for GlobalContextCore.

**Methods** (1):
- `__init__(self, workspace_root, fleet)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `mixins.ContextConsolidationMixin.ContextConsolidationMixin`
- `mixins.ContextDataMixin.ContextDataMixin`
- `mixins.ContextEntityMixin.ContextEntityMixin`
- `mixins.ContextShardMixin.ContextShardMixin`
- `pathlib.Path`
- `src.core.base.Version.VERSION`
- `src.logic.agents.cognitive.context.engines.GlobalContextCore.GlobalContextCore`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/classes/context/GlobalContextEngine.improvements.md

# Improvements for GlobalContextEngine

**File**: `src\classes\context\GlobalContextEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 64 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `GlobalContextEngine_test.py` with pytest tests

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


"""Advanced Long-Term Memory (LTM) for agents.
Consolidates episodic memories into semantic knowledge and persistent preferences.
Inspired by mem0 and BabyAGI patterns.
"""

from pathlib import Path
from typing import Any

from src.core.base.Version import VERSION
from src.logic.agents.cognitive.context.engines.GlobalContextCore import (
    GlobalContextCore,
)

from .mixins.ContextConsolidationMixin import ContextConsolidationMixin
from .mixins.ContextDataMixin import ContextDataMixin
from .mixins.ContextEntityMixin import ContextEntityMixin
from .mixins.ContextShardMixin import ContextShardMixin

__version__ = VERSION


class GlobalContextEngine(
    ContextShardMixin, ContextDataMixin, ContextEntityMixin, ContextConsolidationMixin
):
    """Manages persistent project-wide knowledge and agent preferences.
    Shell for GlobalContextCore.
    """

    def __init__(self, workspace_root: str | None = None, fleet: Any = None) -> None:
        if fleet and hasattr(fleet, "workspace_root"):
            self.workspace_root = Path(fleet.workspace_root)
        elif workspace_root:
            self.workspace_root = Path(workspace_root)
        else:
            self.workspace_root = Path(".")

        self.context_file = self.workspace_root / ".agent_global_context.json"
        self.shard_dir = self.workspace_root / ".agent_shards"
        self.core = GlobalContextCore()
        self.memory: dict[str, Any] = {
            "facts": {},
            "preferences": {},
            "constraints": [],
            "insights": [],
            "entities": {},
            "lessons_learned": [],
        }
        self._loaded_shards: set[Any] = set()
        self.load()
