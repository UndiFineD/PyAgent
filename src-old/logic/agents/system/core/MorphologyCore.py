"""LLM_CONTEXT_START

## Source: src-old/logic/agents/system/core/MorphologyCore.description.md

# MorphologyCore

**File**: `src\\logic\agents\\system\\core\\MorphologyCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 48  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for MorphologyCore.

## Classes (1)

### `MorphologyCore`

MorphologyCore handles agent splitting, merging, and DNA encoding.
It identifies logical overlap and proposes architectural shifts.

**Methods** (3):
- `calculate_path_overlap(self, path_a, path_b)`
- `encode_agent_dna(self, name, tools, prompt, model)`
- `propose_split(self, load_stats)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `json`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/system/core/MorphologyCore.improvements.md

# Improvements for MorphologyCore

**File**: `src\\logic\agents\\system\\core\\MorphologyCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 48 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MorphologyCore_test.py` with pytest tests

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

import json


class MorphologyCore:
    """MorphologyCore handles agent splitting, merging, and DNA encoding.
    It identifies logical overlap and proposes architectural shifts.
    """

    def calculate_path_overlap(self, path_a: list[str], path_b: list[str]) -> float:
        """Calculates Jaccard similarity between two agent logic paths.
        Overlap > 0.8 triggers a 'MERGE' proposal.
        """
        set_a, set_b = set(path_a), set(path_b)
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return intersection / union

    def encode_agent_dna(
        self, name: str, tools: list[str], prompt: str, model: str
    ) -> str:
        """Encodes the agent's DNA into a JSON string.
        """
        dna = {
            "name": name,
            "genome": {
                "tools": sorted(tools),
                "system_prompt_hash": hash(prompt),
                "preferred_model": model,
            },
            "version": "1.0.DNA",
        }
        return json.dumps(dna)

    def propose_split(self, load_stats: dict[str, float]) -> list[str]:
        """If an agent's load is too high, it proposes splitting into sub-specialists.
        """
        proposals = []
        for agent, load in load_stats.items():
            if load > 0.85:
                proposals.append(f"{agent}_Specialist_A")
                proposals.append(f"{agent}_Specialist_B")
        return proposals
