# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified Autonomy and Self-Model core."""

from src.core.base.common.base_core import BaseCore
from typing import List, Optional

class AutonomyCore(BaseCore):
    """
    Standard implementation for Agent Autonomy and Self-Model.
    Provides logic for identifying blind spots and calculating evolution sleep intervals.
    """
    
    def __init__(self, agent_id: str, repo_root: Optional[str] = None):
        super().__init__(name=f"Autonomy-{agent_id}", repo_root=repo_root)
        self.agent_id = agent_id
        self.performance_history: List[float] = []

    def identify_blind_spots(
        self, success_rate: float, task_diversity: float
    ) -> List[str]:
        """Analyzes performance stats to find 'Blind Spots'."""
        blind_spots = []
        if success_rate < 0.7:
            blind_spots.append("GENERAL_REASONING_RELIABILITY")
        if task_diversity < 0.3:
            blind_spots.append("DOMAIN_SPECIFIC_RIGIDITY")
        return blind_spots

    def calculate_daemon_sleep_interval(self, optimization_score: float) -> int:
        """Returns sleep seconds for the Background Evolution Daemon."""
        if optimization_score >= 1.0:
            return 3600  # 1 hour
        elif optimization_score > 0.8:
            return 600  # 10 minutes
        else:
            return 60  # 1 minute (high activity)

    def generate_self_improvement_plan(self, blind_spots: List[str]) -> str:
        """Constructs a directive for the agent to use in its next improvement cycle."""
        plan = f"AGENT SELF-MODEL UPDATE for {self.agent_id}:\n"
        if not blind_spots:
            return f"{plan}Status: Optimal. No immediate changes required."

        plan += "Action: Expand training data for identified blind spots: " + ", ".join(
            blind_spots
        )
        return plan
