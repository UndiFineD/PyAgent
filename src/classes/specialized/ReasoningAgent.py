#!/usr/bin/env python3

"""Agent specializing in logical analysis and hypothesis generation."""

import logging
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

class ReasoningAgent(BaseAgent):
    """Deep reasoning and analysis engine."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Reasoning Agent. "
            "You perform critical analysis of information. "
            "Break down observations into logical steps and identify potential failures."
        )

    @as_tool
    def analyze(self, input_text: str) -> str:
        """Performs logical decomposition and hypothesis formation."""
        return f"### Analytical Breakdown\n1. Input observed: {input_text[:50]}...\n2. Hypothesis: The task is feasible if dependencies are met.\n3. Risk: Incomplete context could lead to partial solution."

    def improve_content(self, prompt: str) -> str:
        return self.analyze(prompt)
