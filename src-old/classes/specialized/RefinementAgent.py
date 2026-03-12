#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/specialized/RefinementAgent.description.md

# RefinementAgent

**File**: `src\classes\specialized\RefinementAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 81  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in Recursive Self-Refinement.
Optimizes system prompts, tool descriptions, and agent logic based on performance telemetry.

## Classes (1)

### `RefinementAgent`

**Inherits from**: BaseAgent

Refines the swarm's core logic and instructions through performance feedback.

**Methods** (5):
- `__init__(self, file_path)`
- `analyze_performance_gaps(self, failure_logs)`
- `propose_prompt_update(self, agent_class_name, performance_feedback)`
- `update_agent_source(self, file_path, new_logic_snippet)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (11):
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/RefinementAgent.improvements.md

# Improvements for RefinementAgent

**File**: `src\classes\specialized\RefinementAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 81 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `RefinementAgent_test.py` with pytest tests

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

"""Agent specializing in Recursive Self-Refinement.
Optimizes system prompts, tool descriptions, and agent logic based on performance telemetry.
"""

import logging
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool


class RefinementAgent(BaseAgent):
    """Refines the swarm's core logic and instructions through performance feedback."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.refinement_logs = Path("logs/self_refinement")
        self.refinement_logs.mkdir(parents=True, exist_ok=True)

        self._system_prompt = (
            "You are the Refinement Agent. "
            "Your role is to iteratively improve the performance of all agents in the fleet. "
            "You analyze execution failures, user feedback, and model hallucinations "
            "to rewrite system prompts, update tool metadata, and suggest logic enhancements."
        )

    @as_tool
    def analyze_performance_gaps(self, failure_logs: str) -> str:
        """Analyzes failure patterns to identify prompt or tool weaknesses."""
        logging.info("Refinement: Analyzing performance gaps...")
        # Simulated analysis
        analysis = (
            "### Refinement Analysis\n"
            "1. Found recurrent 'hallucination' when searching with BrowsingAgent.\n"
            "2. Tool 'execute_sql' in SQLAgent has ambiguous param descriptions.\n"
            "3. System prompt for LinguisticAgent is too verbose."
        )
        return analysis

    @as_tool
    def propose_prompt_update(
        self, agent_class_name: str, performance_feedback: str
    ) -> str:
        """Generates a new optimized system prompt for an agent.
        Args:
            agent_class_name: The name of the agent class to refine.
            performance_feedback: Summary of what the agent is doing wrong.
        """
        logging.info(f"Refinement: Generating new prompt for {agent_class_name}...")

        new_prompt = (
            f"You are the {agent_class_name}. "
            f"Optimized Instructions: Focus on high-precision outputs. "
            f"Avoid verbose explanations. Correct for: {performance_feedback}"
        )

        return f"### Proposed System Prompt for {agent_class_name}\n\n```\n{new_prompt}\n```"

    @as_tool
    def update_agent_source(self, file_path: str, new_logic_snippet: str) -> str:
        """Safely applies a refinement to an agent's source code.
        Args:
            file_path: Absolute path to the agent's Python file.
            new_logic_snippet: The refined code block to inject or update.
        """
        # In a real scenario, this would use the edit tools or AST manipulation.
        # This implementation logs the proposal for human-governed or orchestrated application.
        ref_file = self.refinement_logs / f"refine_{os.path.basename(file_path)}.txt"
        with open(ref_file, "w") as f:
            f.write(new_logic_snippet)

        return f"Refinement logic written to {ref_file}. Verification required before merge."

    def improve_content(self, prompt: str) -> str:
        return "Fleet self-refinement loops are active and monitoring for optimization opportunities."


if __name__ == "__main__":
    from src.classes.base_agent.utilities import create_main_function

    main = create_main_function(
        RefinementAgent, "Refinement Agent", "Autonomous logic optimizer"
    )
    main()
