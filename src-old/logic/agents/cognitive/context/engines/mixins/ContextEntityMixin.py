#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/mixins/ContextEntityMixin.description.md

# ContextEntityMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\mixins\\ContextEntityMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 52  
**Complexity**: 2 (simple)

## Overview

Entity and lesson management logic for GlobalContextEngine.

## Classes (1)

### `ContextEntityMixin`

Mixin for tracking entities and project lessons.

**Methods** (2):
- `add_entity_info(self, entity_name, attributes)`
- `record_lesson(self, failure_context, correction, agent)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `datetime.datetime`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/mixins/ContextEntityMixin.improvements.md

# Improvements for ContextEntityMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\mixins\\ContextEntityMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 52 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextEntityMixin_test.py` with pytest tests

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

"""Entity and lesson management logic for GlobalContextEngine."""

from datetime import datetime
from typing import Any


class ContextEntityMixin:
    """Mixin for tracking entities and project lessons."""

    def add_entity_info(self, entity_name: str, attributes: dict[str, Any]) -> None:
        """Tracks specific entities (files, classes, modules) and their metadata."""
        if not hasattr(self, "memory") or not hasattr(self, "core"):
            return

        existing = self.memory["entities"].get(entity_name, {})
        self.memory["entities"][entity_name] = self.core.merge_entity_info(
            existing, attributes
        )
        if hasattr(self, "save"):
            self.save()

    def record_lesson(self, failure_context: str, correction: str, agent: str) -> None:
        """Records a learned lesson to prevent future errors."""
        if not hasattr(self, "memory") or not hasattr(self, "core"):
            return

        lesson = {
            "failure": failure_context,
            "correction": correction,
            "agent": agent,
            "timestamp": datetime.now().isoformat(),
        }
        self.memory["lessons_learned"].append(lesson)
        self.memory["lessons_learned"] = self.core.prune_lessons(
            self.memory["lessons_learned"]
        )
        if hasattr(self, "save"):
            self.save()
