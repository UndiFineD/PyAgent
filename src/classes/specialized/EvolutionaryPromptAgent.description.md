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
