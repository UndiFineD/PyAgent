#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/cognitive/TheoryOfMindCore.description.md

# TheoryOfMindCore

**File**: `src\classes\cognitive\TheoryOfMindCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 76  
**Complexity**: 3 (simple)

## Overview

TheoryOfMindCore logic for PyAgent.
Pure logic for modeling agent mental states and capabilities.
No I/O or side effects.

## Classes (1)

### `TheoryOfMindCore`

Pure logic core for Theory of Mind modeling.

**Methods** (3):
- `update_profile_logic(profile, observations)`
- `estimate_knowledge_score(profile, topic)`
- `rank_collaborators(profiles, task)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Set`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/classes/cognitive/TheoryOfMindCore.improvements.md

# Improvements for TheoryOfMindCore

**File**: `src\classes\cognitive\TheoryOfMindCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 76 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TheoryOfMindCore_test.py` with pytest tests

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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
TheoryOfMindCore logic for PyAgent.
Pure logic for modeling agent mental states and capabilities.
No I/O or side effects.
"""

from src.core.base.version import VERSION
from typing import Dict, Any, List, Set, Tuple

__version__ = VERSION


class TheoryOfMindCore:
    """Pure logic core for Theory of Mind modeling."""

    @staticmethod
    def update_profile_logic(
        profile: dict[str, Any], observations: dict[str, Any]
    ) -> dict[str, Any]:
        """Core logic to update an agent profile based on observations."""
        # Ensure sets exist
        domains: set[str] = set(profile.get("knowledge_domains", []))
        strengths: set[str] = set(profile.get("strengths", []))
        limitations: set[str] = set(profile.get("limitations", []))

        if "domain" in observations:
            domains.add(observations["domain"])
        if "strength" in observations:
            strengths.add(observations["strength"])
        if "success" in observations:
            if not observations["success"]:
                limitations.add(observations.get("task", "unknown"))

        return {
            "knowledge_domains": list(domains),
            "strengths": list(strengths),
            "limitations": list(limitations),
            "last_active": observations.get(
                "timestamp", profile.get("last_active", 0.0)
            ),
        }

    @staticmethod
    def estimate_knowledge_score(profile: dict[str, Any], topic: str) -> float:
        """Logic for estimating knowledge probability."""
        domains = profile.get("knowledge_domains", [])
        for domain in domains:
            if domain.lower() in topic.lower():
                return 0.9
        return 0.3

    @staticmethod
    def rank_collaborators(profiles: dict[str, dict[str, Any]], task: str) -> list[str]:
        """Logic for ranking agents for a task."""
        rankings: list[tuple[str, float]] = []
        for agent, profile in profiles.items():
            score = TheoryOfMindCore.estimate_knowledge_score(profile, task)
            rankings.append((agent, score))

        return [
            name
            for name, score in sorted(rankings, key=lambda x: x[1], reverse=True)
            if score > 0.5
        ]
