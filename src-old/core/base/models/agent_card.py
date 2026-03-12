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
# See the License for the specific language governing permissions and
# limitations under the License.

"""
LLM_CONTEXT_START

## Source: src-old/core/base/models/agent_card.description.md

# agent_card

**File**: `src\core\base\models\agent_card.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 38  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for agent_card.

## Classes (2)

### `AgentCard`

**Inherits from**: BaseModel

Standardized metadata for an agent in the fleet.
Enables cross-agent discovery and orchestration.
Harvested from .external/agentic_design_patterns pattern.

### `Config`

Class Config implementation.

## Dependencies

**Imports** (7):
- `dataclasses.dataclass`
- `dataclasses.field`
- `pydantic.BaseModel`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/models/agent_card.improvements.md

# Improvements for agent_card

**File**: `src\core\base\models\agent_card.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 38 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: Config

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `agent_card_test.py` with pytest tests

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

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from pydantic import BaseModel


class AgentCard(BaseModel):
    """
    Standardized metadata for an agent in the fleet.
    Enables cross-agent discovery and orchestration.
    Harvested from .external/agentic_design_patterns pattern.
    """

    id: str
    name: str
    version: str = "1.0.0"
    description: str
    tier: str = "specialized"  # specialized, integrated, elite
    skills: List[str] = field(default_factory=list)
    input_modes: List[str] = field(default_factory=lambda: ["text"])
    output_modes: List[str] = field(default_factory=lambda: ["text"])
    config_schema: Dict[str, Any] = field(default_factory=dict)
    owner_team: Optional[str] = None
    last_updated: float = field(default_factory=lambda: 0.0)

    class ConfigDict:
        arbitrary_types_allowed = True
