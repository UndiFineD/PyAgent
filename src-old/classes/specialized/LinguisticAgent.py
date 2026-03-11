#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/LinguisticAgent.description.md

# LinguisticAgent

**File**: `src\classes\specialized\LinguisticAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 41  
**Complexity**: 3 (simple)

## Overview

Agent specializing in linguistic articulation and epistemic subordination.
Ensures that the LLM only verbalizes grounded results and never hallucinates new technical facts.

## Classes (1)

### `LinguisticAgent`

**Inherits from**: BaseAgent

The linguistic surface layer of the PyAgent OS.

**Methods** (3):
- `__init__(self, file_path)`
- `articulate_results(self, technical_report, user_query)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (3):
- `logging`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/LinguisticAgent.improvements.md

# Improvements for LinguisticAgent

**File**: `src\classes\specialized\LinguisticAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 41 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `LinguisticAgent_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""Agent specializing in linguistic articulation and epistemic subordination.
Ensures that the LLM only verbalizes grounded results and never hallucinates new technical facts.
"""

import logging

from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool


class LinguisticAgent(BaseAgent):
    """The linguistic surface layer of the PyAgent OS."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Linguistic Articulation Agent. "
            "Your role is to translate technical reports into natural language for the user. "
            "STRICT RULE: You are epistemically subordinated to the expert agents. "
            "You MUST NOT add facts, extrapolate reasoning, or 'hallucinate' details not present in the input. "
            "If the technical report is empty or says ERROR, you must state that exactly."
        )

    @as_tool
    def articulate_results(self, technical_report: str, user_query: str) -> str:
        """Converts raw expert outputs into a polite, natural response.

        Args:
            technical_report: The raw output from the StructuredOrchestrator.
            user_query: The original user question.

        Return:
            A natural language summary.

        """
        logging.info("LinguisticAgent: Articulating technical report...")

        # In a real implementation, this would call the LLM with the report as context.
        # Here we simulate the constrained linguistic surface.
        return f"Hello! Regarding your request: '{user_query}', I have processed it through the expert systems.\n\nSummary of results:\n{technical_report[:500]}..."

    def improve_content(self, prompt: str) -> str:
        """Entry point for verbalization."""
        return self.articulate_results(prompt, "How can I help you?")
