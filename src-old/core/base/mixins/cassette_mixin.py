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
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""LLM_CONTEXT_START

## Source: src-old/core/base/mixins/cassette_mixin.description.md

# cassette_mixin

**File**: `src\\core\base\\mixins\\cassette_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 43  
**Complexity**: 3 (simple)

## Overview

Mixin regarding Synaptic Modularization (Cassette-based logic).

## Classes (1)

### `CassetteMixin`

Mixin regarding providing Cassette Orchestration capabilities to an Agent.

**Methods** (3):
- `__init__(self)`
- `register_logic_cassette(self, cassette)`
- `has_cassette(self, name)`

## Dependencies

**Imports** (5):
- `src.core.base.logic.cassette_orchestrator.BaseLogicCassette`
- `src.core.base.logic.cassette_orchestrator.CassetteOrchestrator`
- `src.core.base.models.communication_models.CascadeContext`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/cassette_mixin.improvements.md

# Improvements for cassette_mixin

**File**: `src\\core\base\\mixins\\cassette_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 43 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `cassette_mixin_test.py` with pytest tests

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

"""
Mixin regarding Synaptic Modularization (Cassette-based logic).
"""

from typing import Any, Optional

from src.core.base.logic.cassette_orchestrator import (
    BaseLogicCassette,
    CassetteOrchestrator,
)
from src.core.base.models.communication_models import CascadeContext


class CassetteMixin:
    """Mixin regarding providing Cassette Orchestration capabilities to an Agent.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._cassette_orchestrator: CassetteOrchestrator = CassetteOrchestrator()

    def register_logic_cassette(self, cassette: BaseLogicCassette) -> None:
        """Register a specialized logic cassette regarding the agent's synapses."""
        self._cassette_orchestrator.register_cassette(cassette)

    async def execute_cassette(
        self, name: str, data: Any, context: Optional[CascadeContext] = None
    ) -> Any:
        """Execute a specialized logic cassette regarding the provided context."""
        actual_context = context or getattr(self, "context", CascadeContext())
        return await self._cassette_orchestrator.run_cassette(
            name, data, actual_context
        )

    def has_cassette(self, name: str) -> bool:
        """Check if a specific cassette regarding the synapses exists."""
        return self._cassette_orchestrator.get_cassette(name) is not None
