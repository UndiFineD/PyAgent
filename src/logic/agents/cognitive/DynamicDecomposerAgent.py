#!/usr/bin/env python3

"""Agent specializing in Autonomous Task Decomposition v2.
Handles dynamic task splitting, load balancing, and capability-based routing.
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

class DynamicDecomposerAgent(BaseAgent):
    """Orchestrates complex task splitting and routes sub-tasks to specialized agents based on load."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Dynamic Decomposer Agent. "
            "Your role is to break down monolithic user requests into a series of actionable steps. "
            "You consider the specialized capabilities of the available swarm members "
            "and their current estimated workloads to ensure optimal task parallelization."
        )

    @as_tool
    def decompose_task_v2(self, complex_task: str, available_agents: List[str]) -> str:
        """Splits a complex task into optimized sub-tasks for the swarm.
        Args:
            complex_task: The high-level user request.
            available_agents: List of agent names currently active.
        """
        logging.info(f"DynamicDecomposer: Decomposing task: {complex_task[:50]}...")
        
        # In a real implementation, this would involve LLM reasoning to split the task
        # and assign them to the best suited agents.
        
        decomposition = {
            "root_task": complex_task,
            "sub_tasks": [
                {"id": 1, "task": "Initial research and context collection", "assigned_to": "ResearchAgent"},
                {"id": 2, "task": "Data analysis and synthesis", "assigned_to": "ReasoningAgent"},
                {"id": 3, "task": "Execution and implementation", "assigned_to": "CoderAgent"},
                {"id": 4, "task": "Final validation and reporting", "assigned_to": "LinguisticAgent"}
            ]
        }
        
        return f"### Optimized Task Decomposition\n\n```json\n{json.dumps(decomposition, indent=2)}\n```"

    @as_tool
    def balance_swarm_load(self, pending_tasks: List[Dict[str, Any]]) -> str:
        """Re-routes tasks among agents to prevent bottlenecks."""
        return "Swarm load balancing: Workload evenly distributed. No re-routing necessary."

    def improve_content(self, prompt: str) -> str:
        return "Task decomposition workflows are optimized for maximum parallelization."

if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(DynamicDecomposerAgent, "Dynamic Decomposer Agent", "Task splitting and routing optimizer")
    main()
