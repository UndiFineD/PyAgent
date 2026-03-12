#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/cognitive/TheoryOfMind.description.md

# TheoryOfMind

**File**: `src\classes\cognitive\TheoryOfMind.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 61  
**Complexity**: 5 (moderate)

## Overview

Shell for TheoryOfMind, managing agent profiles and state.

## Classes (1)

### `TheoryOfMind`

Models the mental states and knowledge domains of other agents.

Acts as the I/O Shell for TheoryOfMindCore.

**Methods** (5):
- `__init__(self)`
- `update_model(self, agent_name, observations)`
- `estimate_knowledge(self, agent_name, topic)`
- `suggest_collaborator(self, task)`
- `get_mental_map(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.version.VERSION`
- `src.logic.cognitive.TheoryOfMindCore.TheoryOfMindCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/cognitive/TheoryOfMind.improvements.md

# Improvements for TheoryOfMind

**File**: `src\classes\cognitive\TheoryOfMind.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 61 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TheoryOfMind_test.py` with pytest tests

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


"""Shell for TheoryOfMind, managing agent profiles and state."""

from src.core.base.version import VERSION
from typing import Dict, Any, List
from src.logic.cognitive.TheoryOfMindCore import TheoryOfMindCore

__version__ = VERSION


class TheoryOfMind:
    """Models the mental states and knowledge domains of other agents.

    Acts as the I/O Shell for TheoryOfMindCore.
    """

    def __init__(self) -> None:
        self.agent_profiles: dict[str, dict[str, Any]] = {}
        self.core = TheoryOfMindCore()

    def update_model(self, agent_name: str, observations: dict[str, Any]) -> None:
        """Updates the internal model via Core."""
        current_profile = self.agent_profiles.get(
            agent_name,
            {
                "knowledge_domains": [],
                "strengths": [],
                "limitations": [],
                "last_active": 0.0,
            },
        )

        updated = self.core.update_profile_logic(current_profile, observations)
        self.agent_profiles[agent_name] = updated

    def estimate_knowledge(self, agent_name: str, topic: str) -> float:
        """Estimates knowledge probability via Core."""
        if agent_name not in self.agent_profiles:
            return 0.5

        return self.core.estimate_knowledge_score(
            self.agent_profiles[agent_name], topic
        )

    def suggest_collaborator(self, task: str) -> list[str]:
        """Suggests collaborators via Core."""
        return self.core.rank_collaborators(self.agent_profiles, task)

    def get_mental_map(self) -> dict[str, Any]:
        """Returns the collective mental map."""
        # The core already returns serializable lists
        return self.agent_profiles
