"""LLM_CONTEXT_START

## Source: src-old/logic/agents/security/core/ByzantineCore.description.md

# ByzantineCore

**File**: `src\\logic\agents\\security\\core\\ByzantineCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 75  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for ByzantineCore.

## Classes (1)

### `ByzantineCore`

Pure logic for Byzantine Fault Tolerance (BFT) consensus.
Calculates weighted agreement scores and detect malicious deviations.

**Methods** (4):
- `calculate_agreement_score(self, votes)`
- `select_committee(self, agents_reliability, min_size)`
- `get_required_quorum(self, change_type)`
- `detect_deviating_hashes(self, votes, consensus_hash)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/security/core/ByzantineCore.improvements.md

# Improvements for ByzantineCore

**File**: `src\\logic\agents\\security\\core\\ByzantineCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 75 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ByzantineCore_test.py` with pytest tests

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


class ByzantineCore:
    """Pure logic for Byzantine Fault Tolerance (BFT) consensus.
    Calculates weighted agreement scores and detect malicious deviations.
    """

    def calculate_agreement_score(self, votes: list[dict[str, any]]) -> float:
        """Calculates the consensus score.
        votes: list of {'weight': float, 'hash': str}
        """
        if not votes:
            return 0.0

        total_weight = sum(v['weight'] for v in votes)
        hash_weights = {}

        for v in votes:
            h = v['hash']
            hash_weights[h] = hash_weights.get(h, 0.0) + v['weight']

        if not total_weight:
            return 0.0

        max_agreement = max(hash_weights.values())
        return max_agreement / total_weight

    def select_committee(self, agents_reliability: dict[str, float], min_size: int = 3) -> list[str]:
        """Scales the committee based on historic reliability scores.
        Only recruits agents with reliability > 0.7.
        """
        eligible = [(name, score) for name, score in agents_reliability.items() if score > 0.7]
        # Sort by reliability descending
        eligible.sort(key=lambda x: x[1], reverse=True)

        committee = [name for name, _ in eligible]
        if len(committee) < min_size:
            # Fallback to top N if not enough high-reliability agents
            return sorted(agents_reliability.keys(), key=lambda x: agents_reliability[x], reverse=True)[:min_size]

        return committee

    def get_required_quorum(self, change_type: str) -> float:
        """Returns the variable quorum requirement based on the risk level.
        Critical infrastructure: 0.8 (4/5)
        Documentation/Scripts: 0.5 (1/2)
        Default: 0.67 (2/3)
        """
        if change_type in ["infrastructure", "security", "core"]:
            return 0.8
        elif change_type in ["documentation", "examples", "comments"]:
            return 0.5
        return 0.67

    def detect_deviating_hashes(self, votes: list[dict[str, any]], consensus_hash: str) -> list[str]:
        """Returns IDs of agents whose votes deviated from consensus."""
        return [v['id'] for v in votes if v['hash'] != consensus_hash]
