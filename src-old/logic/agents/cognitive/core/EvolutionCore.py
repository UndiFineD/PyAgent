"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/core/EvolutionCore.description.md

# EvolutionCore

**File**: `src\\logic\agents\\cognitive\\core\\EvolutionCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 41  
**Complexity**: 3 (simple)

## Overview

Core logic for Evolutionary Hyper-Parameter Tuning (Phase 182).
Handles prompt crossover and lineage persistence.

## Classes (1)

### `EvolutionCore`

Class EvolutionCore implementation.

**Methods** (3):
- `prompt_crossover(prompt1, prompt2)`
- `calculate_prompt_sha(prompt)`
- `mutate_prompt(prompt, mutation_rate)`

## Dependencies

**Imports** (2):
- `hashlib`
- `random`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/core/EvolutionCore.improvements.md

# Improvements for EvolutionCore

**File**: `src\\logic\agents\\cognitive\\core\\EvolutionCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 41 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: EvolutionCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `EvolutionCore_test.py` with pytest tests

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

"""
Core logic for Evolutionary Hyper-Parameter Tuning (Phase 182).
Handles prompt crossover and lineage persistence.
"""

import hashlib
import random


class EvolutionCore:
    @staticmethod
    def prompt_crossover(prompt1: str, prompt2: str) -> str:
        """Combines two prompts by interweaving their logical blocks.
        """
        lines1 = prompt1.splitlines()
        lines2 = prompt2.splitlines()

        # Take halves or interweave
        mid1 = len(lines1) // 2
        mid2 = len(lines2) // 2

        child_lines = lines1[:mid1] + lines2[mid2:]
        return "\n".join(child_lines)

    @staticmethod
    def calculate_prompt_sha(prompt: str) -> str:
        """Returns a short SHA hash of the prompt for lineage tracking.
        """
        return hashlib.sha256(prompt.encode()).hexdigest()[:12]

    @staticmethod
    def mutate_prompt(prompt: str, mutation_rate: float = 0.1) -> str:
        """Randomly injects keywords or modifies tone.
        """
        modifiers = [
            "be more precise",
            "explain reasoning",
            "be concise",
            "check for security",
        ]
        if random.random() < mutation_rate:
            return prompt + f"\n[Mutation: {random.choice(modifiers)}]"
        return prompt
