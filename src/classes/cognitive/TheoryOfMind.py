#!/usr/bin/env python3

"""Theory of Mind (ToM) module for agent-to-agent reasoning.
Tracks what other agents 'know' or their specialized capabilities.
"""

import logging
from typing import Dict, Any, List, Set

class TheoryOfMind:
    """Models the mental states and knowledge domains of other agents."""

    def __init__(self) -> None:
        self.agent_profiles: Dict[str, Dict[str, Any]] = {}

    def update_model(self, agent_name: str, observations: Dict[str, Any]) -> None:
        """Updates the internal model of another agent based on observed behavior."""
        if agent_name not in self.agent_profiles:
            self.agent_profiles[agent_name] = {
                "knowledge_domains": set(),
                "strengths": set(),
                "limitations": set(),
                "last_active": 0.0
            }
            
        profile = self.agent_profiles[agent_name]
        
        if "domain" in observations:
            profile["knowledge_domains"].add(observations["domain"])
        if "strength" in observations:
            profile["strengths"].add(observations["strength"])
        if "success" in observations:
            if observations["success"]:
                profile["last_active"] = observations.get("timestamp", 0)
            else:
                profile["limitations"].add(observations.get("task", "unknown"))

    def estimate_knowledge(self, agent_name: str, topic: str) -> float:
        """Estimates how likely an agent is to know about a specific topic."""
        if agent_name not in self.agent_profiles:
            return 0.5 # Neutral expectation
            
        profile = self.agent_profiles[agent_name]
        for domain in profile["knowledge_domains"]:
            if domain.lower() in topic.lower():
                return 0.9
                
        return 0.3 # Lower expectation if topic is outside known domains

    def suggest_collaborator(self, task: str) -> List[str]:
        """Suggests the best agents to collaborate with based on the ToM model."""
        rankings = []
        for agent, profile in self.agent_profiles.items():
            score = self.estimate_knowledge(agent, task)
            rankings.append((agent, score))
            
        return [name for name, score in sorted(rankings, key=lambda x: x[1], reverse=True) if score > 0.5]

    def get_mental_map(self) -> Dict[str, Any]:
        """Returns a serializable version of the Theory of Mind map."""
        serializable = {}
        for name, profile in self.agent_profiles.items():
            serializable[name] = {
                "domains": list(profile["knowledge_domains"]),
                "strengths": list(profile["strengths"]),
                "limitations": list(profile["limitations"])
            }
        return serializable
