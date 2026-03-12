"""LLM_CONTEXT_START

## Source: src-old/core/base/registry.description.md

# registry

**File**: `src\\core\base\registry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 62  
**Complexity**: 6 (moderate)

## Overview

AgentRegistry: Central registry for all active agent instances.
Provides discovery and cross-agent communication.

## Classes (1)

### `AgentRegistry`

Singleton registry to track all active agents.

**Methods** (6):
- `__new__(cls)`
- `register(self, agent)`
- `unregister(self, name)`
- `get_agent(self, name)`
- `list_agents(self)`
- `active_count(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/core/base/registry.improvements.md

# Improvements for registry

**File**: `src\\core\base\registry.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 62 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `registry_test.py` with pytest tests

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


"""
AgentRegistry: Central registry for all active agent instances.
Provides discovery and cross-agent communication.
"""

import logging

from src.core.base.BaseAgent import BaseAgent
from src.core.base.version import VERSION

__version__ = VERSION

class AgentRegistry:
    """Singleton registry to track all active agents."""

    _instance: AgentRegistry | None = None
    _agents: dict[str, BaseAgent] = {}

    def __new__(cls) -> AgentRegistry:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, agent: BaseAgent) -> None:
        """Register an agent instance."""
        name = getattr(agent, "agent_name", str(id(agent)))
        self._agents[name] = agent
        logging.debug(f"Agent '{name}' registered.")

    def unregister(self, name: str) -> None:
        """Unregister an agent instance."""
        if name in self._agents:
            del self._agents[name]
            logging.debug(f"Agent '{name}' unregistered.")

    def get_agent(self, name: str) -> BaseAgent | None:
        """Retrieve an agent by name."""
        return self._agents.get(name)

    def list_agents(self) -> list[str]:
        """List names of all registered agents."""
        return list(self._agents.keys())

    @property
    def active_count(self) -> int:
        return len(self._agents)
