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

"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/evolution_core.description.md

# evolution_core

**File**: `src\\core\base\\logic\\core\\evolution_core.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 89  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for evolution_core.

## Classes (2)

### `AgentMetadata`

Class AgentMetadata implementation.

### `EvolutionCore`

Manages the lifecycle and evolution of agents based on task performance.
Harvested from self-evolving-subagent patterns.

**Methods** (4):
- `__init__(self, sop_core)`
- `record_usage(self, agent_name, success)`
- `_check_promotion(self, meta)`
- `propose_integration(self, agent_a_name, agent_b_name)`

## Dependencies

**Imports** (7):
- `dataclasses.dataclass`
- `dataclasses.field`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/evolution_core.improvements.md

# Improvements for evolution_core

**File**: `src\\core\base\\logic\\core\\evolution_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 89 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: AgentMetadata

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `evolution_core_test.py` with pytest tests

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

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentMetadata:
    name: str
    usage_count: int = 0
    success_rate: float = 0.0
    last_used: float = field(default_factory=time.time)
    tier: str = "specialized"  # specialized, integrated, elite
    parent_agents: List[str] = field(default_factory=list)
    sop_name: Optional[str] = None


class EvolutionCore:
    """Manages the lifecycle and evolution of agents based on task performance.
    Harvested from self-evolving-subagent patterns.
    """

    def __init__(self, sop_core: Optional[Any] = None):
        self.agent_pool: Dict[str, AgentMetadata] = {}
        self.sop_core = sop_core

    def record_usage(self, agent_name: str, success: bool):
        if agent_name not in self.agent_pool:
            self.agent_pool[agent_name] = AgentMetadata(name=agent_name)

        meta = self.agent_pool[agent_name]
        meta.usage_count += 1
        meta.last_used = time.time()

        # Simple moving average for success rate
        alpha = 0.2
        meta.success_rate = (alpha * (1.0 if success else 0.0)) + (
            (1 - alpha) * meta.success_rate
        )

        if self.sop_core and meta.sop_name:
            self.sop_core.update_sop_metrics(meta.sop_name, success)

        self._check_promotion(meta)

    def _check_promotion(self, meta: AgentMetadata):
        """Promotes agents based on usage and success."""
        if (
            meta.tier == "specialized"
            and meta.usage_count >= 5
            and meta.success_rate >= 0.8
        ):
            meta.tier = "elite"

    def propose_integration(
        self, agent_a_name: str, agent_b_name: str
    ) -> Optional[str]:
        """Proposes a merger of two agents and their SOPs.
        Pattern harvested from self-evolving-subagent.
        """
        meta_a = self.agent_pool.get(agent_a_name)
        meta_b = self.agent_pool.get(agent_b_name)

        if not meta_a or not meta_b:
            return None

        if meta_a.usage_count > 3 and meta_b.usage_count > 3:
            new_name = f"integrated_{agent_a_name}_{agent_b_name}"
            new_sop_name = None

            if self.sop_core and meta_a.sop_name and meta_b.sop_name:
                new_sop_name = f"sop_{new_name}"
                self.sop_core.merge_sops(meta_a.sop_name, meta_b.sop_name, new_sop_name)

            if new_name not in self.agent_pool:
                self.agent_pool[new_name] = AgentMetadata(
                    name=new_name,
                    tier="integrated",
                    usage_count=max(meta_a.usage_count, meta_b.usage_count),
                    parent_agents=[agent_a_name, agent_b_name],
                    sop_name=new_sop_name,
                )
            return new_name

        return None
