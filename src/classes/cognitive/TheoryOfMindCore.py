#!/usr/bin/env python3

"""
TheoryOfMindCore logic for PyAgent.
Pure logic for modeling agent mental states and capabilities.
No I/O or side effects.
"""

from typing import Dict, Any, List, Set, Tuple

class TheoryOfMindCore:
    """Pure logic core for Theory of Mind modeling."""

    @staticmethod
    def update_profile_logic(profile: Dict[str, Any], observations: Dict[str, Any]) -> Dict[str, Any]:
        """Core logic to update an agent profile based on observations."""
        # Ensure sets exist
        domains: Set[str] = set(profile.get("knowledge_domains", []))
        strengths: Set[str] = set(profile.get("strengths", []))
        limitations: Set[str] = set(profile.get("limitations", []))
        
        if "domain" in observations:
            domains.add(observations["domain"])
        if "strength" in observations:
            strengths.add(observations["strength"])
        if "success" in observations:
            if not observations["success"]:
                limitations.add(observations.get("task", "unknown"))
                
        return {
            "knowledge_domains": list(domains),
            "strengths": list(strengths),
            "limitations": list(limitations),
            "last_active": observations.get("timestamp", profile.get("last_active", 0.0))
        }

    @staticmethod
    def estimate_knowledge_score(profile: Dict[str, Any], topic: str) -> float:
        """Logic for estimating knowledge probability."""
        domains = profile.get("knowledge_domains", [])
        for domain in domains:
            if domain.lower() in topic.lower():
                return 0.9
        return 0.3

    @staticmethod
    def rank_collaborators(profiles: Dict[str, Dict[str, Any]], task: str) -> List[str]:
        """Logic for ranking agents for a task."""
        rankings: List[Tuple[str, float]] = []
        for agent, profile in profiles.items():
            score = TheoryOfMindCore.estimate_knowledge_score(profile, task)
            rankings.append((agent, score))
            
        return [name for name, score in sorted(rankings, key=lambda x: x[1], reverse=True) if score > 0.5]
