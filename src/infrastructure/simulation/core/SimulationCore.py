
"""
Core logic for Swarm Simulation and Stress-Testing (Phase 181).
Handles stochastic failure modeling and visualization progress hooks.
"""

import random
from typing import List

class SimulationCore:
    @staticmethod
    def calculate_stochastic_failures(agent_count: int, failure_rate: float = 0.1) -> List[int]:
        """
        Returns a list of agent indices that are designated to 'fail'.
        """
        num_failures = int(agent_count * failure_rate)
        return random.sample(range(agent_count), num_failures)

    @staticmethod
    def apply_latency_spike(base_latency: float, spike_probability: float = 0.05) -> float:
        """
        Simulates network/hardware jitter by adding a random spike.
        """
        if random.random() < spike_probability:
            return base_latency * (1.5 + random.random() * 2.0)
        return base_latency

    @staticmethod
    def format_progress_bar(current: int, total: int, width: int = 40) -> str:
        """
        Generates a simple ASCII progress bar.
        """
        percent = current / total
        filled = int(width * percent)
        bar = "=" * filled + "-" * (width - filled)
        return f"[{bar}] {percent*100:3.0f}% ({current}/{total})"