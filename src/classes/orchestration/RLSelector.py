#!/usr/bin/env python3

"""Reinforcement Learning based tool selector.
Optimizes tool selection by weighting success rates and historical performance.
"""

import logging
import random
from typing import Dict, List, Any, Optional

class RLSelector:
    """Uses a Multi-Armed Bandit strategy to optimize tool selection."""
    
    def __init__(self) -> None:
        # schema: {tool_name: {"success_count": int, "total_calls": int, "weight": float}}
        self.tool_stats: Dict[str, Dict[str, Any]] = {}
        self.epsilon = 0.1  # Exploration rate

    def update_stats(self, tool_name: str, success: bool) -> str:
        """Updates the performance statistics for a tool."""
        if tool_name not in self.tool_stats:
            self.tool_stats[tool_name] = {"success_count": 0, "total_calls": 0, "weight": 1.0}
            
        stats = self.tool_stats[tool_name]
        stats["total_calls"] += 1
        if success:
            stats["success_count"] += 1
            
        # Update weight based on success rate
        stats["weight"] = stats["success_count"] / stats["total_calls"]
        logging.info(f"RL-SELECTOR: Updated {tool_name} weight to {stats['weight']:.2f}")

    def select_best_tool(self, candidate_tools: List[str]) -> str:
        """Selects the optimal tool from a list of candidates."""
        if not candidate_tools:
            raise ValueError("No candidate tools provided.")
            
        # Epsilon-greedy selection
        if random.random() < self.epsilon:
            logging.info("RL-SELECTOR: Exploring random tool.")
            return random.choice(candidate_tools)
            
        # Select tool with highest weight
        best_tool = candidate_tools[0]
        max_weight = -1.0
        
        for tool in candidate_tools:
            weight = self.tool_stats.get(tool, {}).get("weight", 0.5) # Default 0.5 for new tools
            if weight > max_weight:
                max_weight = weight
                best_tool = tool
                
        logging.info(f"RL-SELECTOR: Selected best tool '{best_tool}' (Weight: {max_weight:.2f})")
        return best_tool

    def get_policy_summary(self) -> str:
        """Returns a summary of the current selection policy."""
        summary = ["## Tool Selection Policy (RL)"]
        for tool, stats in self.tool_stats.items():
            summary.append(f"- **{tool}**: Success Rate {stats['weight']*100:.1f}% ({stats['total_calls']} calls)")
        return "\n".join(summary) if len(summary) > 1 else "No policy data yet."
