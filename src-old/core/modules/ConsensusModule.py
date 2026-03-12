r"""LLM_CONTEXT_START

## Source: src-old/core/modules/ConsensusModule.description.md

# ConsensusModule

**File**: `src\core\modules\ConsensusModule.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 78  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for ConsensusModule.

## Classes (1)

### `ConsensusModule`

**Inherits from**: BaseModule

Consolidated core module for consensus protocols.
Migrated from ConsensusCore.

**Methods** (5):
- `initialize(self)`
- `execute(self, proposals, weights)`
- `calculate_winner(self, proposals, weights)`
- `get_agreement_score(self, proposals, winner)`
- `shutdown(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.modules.BaseModule`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/modules/ConsensusModule.improvements.md

# Improvements for ConsensusModule

**File**: `src\core\modules\ConsensusModule.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 78 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ConsensusModule_test.py` with pytest tests

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
from typing import Any

from src.core.base.modules import BaseModule


class ConsensusModule(BaseModule):
    """Consolidated core module for consensus protocols.
    Migrated from ConsensusCore.
    """

    def initialize(self) -> bool:
        """Initialize voting parameters."""
        self.mode = self.config.get("mode", "plurality")
        return super().initialize()

    def execute(
        self, proposals: list[str], weights: list[float] | None = None
    ) -> dict[str, Any]:
        """Executes the consensus protocol to find a winner.
        """
        if not self.initialized:
            self.initialize()

        winner = self.calculate_winner(proposals, weights)
        score = self.get_agreement_score(proposals, winner)

        return {
            "winner": winner,
            "agreement_score": score,
            "quorum_reached": score >= 0.667,  # BFT 2/3 requirement
        }

    def calculate_winner(
        self, proposals: list[str], weights: list[float] | None = None
    ) -> str:
        """Determines the winning proposal based on voting rules."""
        if not proposals:
            return ""

        if weights and len(weights) != len(proposals):
            weights = None

        counts: dict[str, float] = {}
        for idx, p in enumerate(proposals):
            weight = weights[idx] if weights else 1.0
            counts[p] = counts.get(p, 0) + weight

        winner = sorted(counts.keys(), key=lambda x: (counts[x], len(x)), reverse=True)[
            0
        ]

        return winner

    def get_agreement_score(self, proposals: list[str], winner: str) -> float:
        """Calculates the percentage of agents that agreed with the winner."""
        if not proposals:
            return 0.0
        match_count = sum(1 for p in proposals if p == winner)
        return match_count / len(proposals)

    def shutdown(self) -> bool:
        """Cleanup consensus resources."""
        return super().shutdown()
