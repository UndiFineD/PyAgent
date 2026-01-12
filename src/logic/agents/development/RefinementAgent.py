#!/usr/bin/env python3
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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Agent specializing in Recursive Self-Refinement.
Optimizes system prompts, tool descriptions, and agent logic based on performance telemetry.
"""



import logging
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

class RefinementAgent(BaseAgent):
    """Refines the swarm's core logic and instructions through performance feedback."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.refinement_logs = Path("data/logs/self_refinement")
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
    def propose_prompt_update(self, agent_class_name: str, performance_feedback: str) -> str:
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
    from src.core.base.utilities import create_main_function
    main = create_main_function(RefinementAgent, "Refinement Agent", "Autonomous logic optimizer")
    main()
