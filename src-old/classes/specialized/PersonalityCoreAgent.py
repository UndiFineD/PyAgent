#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/PersonalityCoreAgent.description.md

# PersonalityCoreAgent

**File**: `src\classes\specialized\PersonalityCoreAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 87  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for PersonalityCoreAgent.

## Classes (1)

### `PersonalityCoreAgent`

**Inherits from**: BaseAgent

Manages the 'emotional intelligence' and 'vibes' of the fleet.
Adjusts communication style and task priorities based on user context.

**Methods** (3):
- `__init__(self, file_path)`
- `set_vibe_track(self, user_input)`
- `get_track_guidance(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/PersonalityCoreAgent.improvements.md

# Improvements for PersonalityCoreAgent

**File**: `src\classes\specialized\PersonalityCoreAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 87 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `PersonalityCoreAgent_test.py` with pytest tests

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

import logging
from typing import Any

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

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
from src.core.base.version import VERSION

__version__ = VERSION


class PersonalityCoreAgent(BaseAgent):
    """Manages the 'emotional intelligence' and 'vibes' of the fleet.
    Adjusts communication style and task priorities based on user context.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Fleet Personality Core. "
            "Your job is to detect the user's emotional state, urgency, and technical level. "
            "You broadcast 'vibe' signals that other agents use to adjust their tone and depth."
        )
        self.current_vibe = "neutral"

    @as_tool
    def set_vibe_track(self, user_input: str) -> dict[str, Any]:
        """Analyzes user input and sets the fleet-wide emotional/operational vibe.
        """
        logging.info(f"PersonalityCoreAgent: Analyzing vibe for: {user_input[:50]}...")

        # In a real implementation, we'd use LLM to classify sentiment/urgency
        # prompt = f"Analyze setiment/urgency of: {user_input}"
        # analysis = self.think(prompt)

        # Simulated analysis logic
        vibe = "professional"
        urgency = "low"

        if any(
            word in user_input.lower()
            for word in ["urgent", "asap", "emergency", "broken"]
        ):
            urgency = "high"
            vibe = "rapid_response"
        elif any(
            word in user_input.lower() for word in ["thanks", "great", "awesome", "fun"]
        ):
            vibe = "friendly"

        self.current_vibe = vibe

        # Emit signal to the fleet
        if hasattr(self, "registry") and self.registry:
            self.registry.emit(
                "FLEET_VIBE_CHANGED",
                {"vibe": vibe, "urgency": urgency, "context": user_input[:100]},
            )

        return {"status": "success", "detected_vibe": vibe, "urgency": urgency}

    @as_tool
    def get_track_guidance(self) -> str:
        """Returns instructions for other agents on how to behave under the current vibe.
        """
        guidance = {
            "professional": "Direct, technical, and concise.",
            "friendly": "Encouraging, helpful, and personable.",
            "rapid_response": "Extremely concise, focusing on immediate fixes and safety.",
        }
        return guidance.get(
            self.current_vibe, "Maintain standard operational parameters."
        )
