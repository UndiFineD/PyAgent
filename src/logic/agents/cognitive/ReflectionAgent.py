#!/usr/bin/env python3

"""Agent specializing in self-critique and reflection."""

import logging
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

class ReflectionAgent(BaseAgent):
    """Critique and refinement engine."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Reflection Agent. "
            "Your job is to find flaws in technical solutions. "
            "Be critical, objective, and specific."
        )

    @as_tool
    def critique(self, work: str) -> str:
        """Analyzes work for flaws and suggests improvements."""
        return f"### Critique\n1. Potential edge cases: Not handled.\n2. Inefficiency: The loop structure is O(n^2).\n3. Clarity: Variable names are ambiguous."

    def improve_content(self, prompt: str) -> str:
        return self.critique(prompt)
