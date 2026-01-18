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


"""Reinforcement Learning based tool selector.
Optimizes tool selection by weighting success rates and historical performance.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import random
from typing import Dict, List, Any

__version__ = VERSION

class RLSelector:
    """Uses Bayesian Thompson Sampling to optimize tool selection under uncertainty."""
    
    def __init__(self) -> None:
        # Bayesian parameters for Beta distribution: alpha (successes), beta (failures)
        # schema: {tool_name: {"alpha": float, "beta": float, "total_calls": int}}
        self.tool_stats: dict[str, dict[str, Any]] = {}

    def update_stats(self, tool_name: str, success: bool) -> None:
        """Updates the posterior beliefs for a tool using Bayesian inference."""
        if tool_name not in self.tool_stats:
            # Prior: Beta(1, 1) is a flat uniform prior
            self.tool_stats[tool_name] = {"alpha": 1.0, "beta": 1.0, "total_calls": 0}
            
        stats = self.tool_stats[tool_name]
        stats["total_calls"] += 1
        if success:
            stats["alpha"] += 1.0
        else:
            stats["beta"] += 1.0
            
        weight = stats["alpha"] / (stats["alpha"] + stats["beta"])
        logging.info(f"RL-SELECTOR: Updated Bayesian posterior for {tool_name} (Expected Success: {weight:.2f})")

    def select_best_tool(self, candidate_tools: list[str]) -> str:
        """
        Selects the optimal tool from a list of candidates using Thompson Sampling.
        Samples from each candidate's posterior Beta distribution and picks the max.
        """
        if not candidate_tools:
            raise ValueError("No candidate tools provided.")
            
        best_tool = candidate_tools[0]
        max_sample = -1.0
        
        for tool in candidate_tools:
            if tool not in self.tool_stats:
                self.tool_stats[tool] = {"alpha": 1.0, "beta": 1.0, "total_calls": 0}
            
            stats = self.tool_stats[tool]
            # Thompson Sampling: Sample from Beta(alpha, beta)
            sample = random.betavariate(stats["alpha"], stats["beta"])
            
            if sample > max_sample:
                max_sample = sample
                best_tool = tool
                
        logging.info(f"RL-SELECTOR: Thompson Sampling selected '{best_tool}' (Sample value: {max_sample:.2f})")
        return best_tool

    def get_policy_summary(self) -> str:
        """Returns a summary of the current selection policy."""
        summary = ["## Tool Selection Policy (Bayesian Thompson Sampling)"]
        for tool, stats in self.tool_stats.items():
            expected = stats["alpha"] / (stats["alpha"] + stats["beta"])
            summary.append(f"- **{tool}**: Expected Success Rate {expected*100:.1f}% ({stats['total_calls']} calls)")
        return "\n".join(summary) if len(summary) > 1 else "No policy data yet."

if __name__ == "__main__":
    # Internal test for Bayesian Thompson Sampling
    logging.basicConfig(level=logging.INFO)
    rl = RLSelector()
    rl.update_stats("tool_a", True)
    rl.update_stats("tool_a", True)
    rl.update_stats("tool_a", False)
    rl.update_stats("tool_b", False)
    print(rl.get_policy_summary())
    print(f"Sampled winner: {rl.select_best_tool(['tool_a', 'tool_b'])}")