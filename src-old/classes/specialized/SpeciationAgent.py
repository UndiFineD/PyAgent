#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/SpeciationAgent.description.md

# SpeciationAgent

**File**: `src\classes\specialized\SpeciationAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 50  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for SpeciationAgent.

## Classes (1)

### `SpeciationAgent`

**Inherits from**: BaseAgent

Agent responsible for 'speciation' - creating specialized derivatives of existing agents.
It analyzes task success and generates new agent classes with optimized system prompts.

**Methods** (2):
- `__init__(self, file_path)`
- `evolve_specialized_agent(self, base_agent_name, niche_domain)`

## Dependencies

**Imports** (9):
- `logging`
- `os`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/SpeciationAgent.improvements.md

# Improvements for SpeciationAgent

**File**: `src\classes\specialized\SpeciationAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 50 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SpeciationAgent_test.py` with pytest tests

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

import logging

from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool


class SpeciationAgent(BaseAgent):
    """Agent responsible for 'speciation' - creating specialized derivatives of existing agents.
    It analyzes task success and generates new agent classes with optimized system prompts.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Speciation Agent. "
            "Your goal is to foster agent evolution by identifying niche capabilities "
            "and synthesizing new, specialized agent types from existing 'Base' agents."
        )

    @as_tool
    def evolve_specialized_agent(self, base_agent_name: str, niche_domain: str) -> str:
        """Creates a new agent class file that specializes in a specific niche.
        e.g., 'CoderAgent' -> 'ReactSpecialistAgent'
        """
        logging.info(
            f"SpeciationAgent: Evolving specialization for {base_agent_name} in {niche_domain}"
        )

        new_agent_name = f"{niche_domain.replace(' ', '')}{base_agent_name}"
        output_path = f"src/classes/specialized/{new_agent_name}.py"

        # Generation Logic
        prompt = (
            f"Create a Python class definition for '{new_agent_name}' that inherits from '{base_agent_name}'. "
            f"The specialization niche is: {niche_domain}.\n"
            "Include an optimized __init__ with a specialized _system_prompt.\n"
            "Return ONLY the Python code."
        )

        specialized_code = self.think(prompt)

        # In a real scenario, we'd save this to a file and register it.
        # For now, we simulate the 'speciation' by logging the creation.
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(specialized_code)

        return f"Successfully speciated {new_agent_name} at {output_path}"
