#!/usr/bin/env python3

"""
MemoryCore logic for PyAgent.
Handles episode structuring, utility scoring, and rank-based filtering.
"""

from __future__ import annotations

from typing import Dict, List, Any, Optional
from datetime import datetime

class MemoryCore:
    def __init__(self, baseline_utility: float = 0.5) -> None:
        self.baseline_utility = baseline_utility

    def create_episode(self, agent_name: str, task: str, outcome: str, success: bool, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Pure logic to construct an episode and calculate utility."""
        timestamp = datetime.now().isoformat()
        utility_score = self.baseline_utility
        
        if success:
            utility_score += 0.2
        else:
            utility_score -= 0.3
            
        return {
            "timestamp": timestamp,
            "agent": agent_name,
            "task": task,
            "outcome": outcome,
            "success": success,
            "utility_score": max(0.0, min(1.0, utility_score)),
            "metadata": metadata or {}
        }

    def format_for_indexing(self, episode: Dict[str, Any]) -> str:
        """Standardized string representation for vector databases."""
        return (
            f"Agent: {episode['agent']}\n"
            f"Task: {episode['task']}\n"
            f"Outcome: {episode['outcome']}\n"
            f"Success: {episode['success']}"
        )

    def calculate_new_utility(self, old_score: float, increment: float) -> float:
        """Logic for utility score decay/boost."""
        return max(0.0, min(1.0, old_score + increment))

    def filter_relevant_memories(self, memories: List[Dict[str, Any]], min_utility: float = 0.3) -> List[Dict[str, Any]]:
        """Filters memories by utility threshold."""
        return [m for m in memories if m.get('utility_score', 0.0) >= min_utility]
