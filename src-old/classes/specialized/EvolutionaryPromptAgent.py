#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/EvolutionaryPromptAgent.description.md

# EvolutionaryPromptAgent

**File**: `src\classes\specialized\EvolutionaryPromptAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 125  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for EvolutionaryPromptAgent.

## Classes (1)

### `EvolutionaryPromptAgent`

**Inherits from**: BaseAgent

Agent that implements genetic algorithms to 'breed' and evolve system prompts.
It tracks fitness scores based on task performance and performs crossover/mutation.

**Methods** (5):
- `__init__(self, file_path)`
- `initialize_population(self, seed_prompt)`
- `record_fitness(self, prompt_index, score)`
- `evolve_generation(self)`
- `get_best_prompt(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `random`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.core.EvolutionCore.EvolutionCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/EvolutionaryPromptAgent.improvements.md

# Improvements for EvolutionaryPromptAgent

**File**: `src\classes\specialized\EvolutionaryPromptAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 125 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `EvolutionaryPromptAgent_test.py` with pytest tests

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

import random
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
from src.logic.agents.cognitive.core.EvolutionCore import EvolutionCore

__version__ = VERSION

# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


class EvolutionaryPromptAgent(BaseAgent):
    """Agent that implements genetic algorithms to 'breed' and evolve system prompts.
    It tracks fitness scores based on task performance and performs crossover/mutation.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.population: list[dict[str, Any]] = []
        self.generation = 0
        self.population_size = 10
        self.core = EvolutionCore()
        self._system_prompt = (
            "You are the Evolutionary Prompt Agent. "
            "Your mission is to optimize agent performance by evolving system prompts. "
            "You use fitness scores, mutation, and crossover to generate superior agent instructions."
        )

    @as_tool
    def initialize_population(self, seed_prompt: str) -> str:
        """Creates an initial population of variations of a seed prompt.
        """
        self.population = []
        for i in range(self.population_size):
            # Create a variation (mocked with simple string additions for initialization)
            variation = (
                seed_prompt
                + f"\n[Variation {i}: Focus on specific detail {random.randint(1,100)}]"
            )
            self.population.append({"prompt": variation, "fitness": 0.0, "history": []})
        self.generation = 1
        return (
            f"Initialized population of {self.population_size} prompts for evolution."
        )

    @as_tool
    def record_fitness(self, prompt_index: int, score: float) -> str:
        """Records the performance score (fitness) of a specific prompt in the population.
        """
        if 0 <= prompt_index < len(self.population):
            self.population[prompt_index]["fitness"] = score
            self.population[prompt_index]["history"].append(score)
            return f"Recorded fitness of {score} for prompt {prompt_index}."
        return "Invalid prompt index."

    @as_tool
    def evolve_generation(self) -> dict[str, Any]:
        """Performs selection, crossover, and mutation to create next generation (Phase 182).
        """
        if not self.population:
            return {"error": "Population not initialized."}

        # 1. Selection
        self.population.sort(key=lambda x: x.get("fitness", 0), reverse=True)
        winners = self.population[: self.population_size // 2]

        new_population = []
        for i in range(self.population_size):
            parent1 = random.choice(winners)
            parent2 = random.choice(winners)

            # Crossover & Mutation using Core
            child_prompt = self.core.prompt_crossover(
                parent1["prompt"], parent2["prompt"]
            )
            child_prompt = self.core.mutate_prompt(child_prompt)

            # Lineage Tracking
            sha = self.core.calculate_prompt_sha(child_prompt)
            new_population.append(
                {
                    "prompt": child_prompt,
                    "sha": sha,
                    "parents": [parent1.get("sha"), parent2.get("sha")],
                    "fitness": 0.0,
                    "generation": self.generation + 1,
                }
            )

        self.population = new_population
        self.generation += 1

        return {
            "generation": self.generation,
            "best_fitness_last_gen": winners[0]["fitness"],
            "new_population_size": len(self.population),
        }

    @as_tool
    def get_best_prompt(self) -> str:
        """Returns the prompt with the highest fitness found so far.
        """
        if not self.population:
            return "No population initialized."
        best = max(self.population, key=lambda x: x["fitness"])
        return best["prompt"]
