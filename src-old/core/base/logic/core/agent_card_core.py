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

r"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/agent_card_core.description.md

# agent_card_core

**File**: `src\\core\base\\logic\\core\agent_card_core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 6 imports  
**Lines**: 62  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for agent_card_core.

## Classes (3)

### `AgentCapability`

**Inherits from**: BaseModel

Class AgentCapability implementation.

### `AgentCard`

**Inherits from**: BaseModel

Standardized manifest for cross-agent discovery.
Pattern harvested from agentic_design_patterns.

### `AgentCardCore`

Manages a registry of AgentCards for inter-agent communication (A2A).

**Methods** (5):
- `__init__(self)`
- `register_agent(self, card)`
- `find_agents_by_capability(self, capability_query)`
- `get_agent_manifest(self, agent_id)`
- `export_all_cards(self)`

## Dependencies

**Imports** (6):
- `pydantic.BaseModel`
- `pydantic.Field`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/agent_card_core.improvements.md

# Improvements for agent_card_core

**File**: `src\\core\base\\logic\\core\agent_card_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 62 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: AgentCapability

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `agent_card_core_test.py` with pytest tests

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
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentCapability(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    returns: str = "Any"


class AgentCard(BaseModel):
    """
    """
