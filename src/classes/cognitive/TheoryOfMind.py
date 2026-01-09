#!/usr/bin/env python3

"""Shell for TheoryOfMind, managing agent profiles and state."""

import logging
from typing import Dict, Any, List, Optional

from src.classes.cognitive.TheoryOfMindCore import TheoryOfMindCore

class TheoryOfMind:
    """Models the mental states and knowledge domains of other agents.
    
    Acts as the I/O Shell for TheoryOfMindCore.
    """

    def __init__(self) -> None:
        self.agent_profiles: Dict[str, Dict[str, Any]] = {}
        self.core = TheoryOfMindCore()

    def update_model(self, agent_name: str, observations: Dict[str, Any]) -> None:
        """Updates the internal model via Core."""
        current_profile = self.agent_profiles.get(agent_name, {
            "knowledge_domains": [],
            "strengths": [],
            "limitations": [],
            "last_active": 0.0
        })
        
        updated = self.core.update_profile_logic(current_profile, observations)
        self.agent_profiles[agent_name] = updated

    def estimate_knowledge(self, agent_name: str, topic: str) -> float:
        """Estimates knowledge probability via Core."""
        if agent_name not in self.agent_profiles:
            return 0.5
            
        return self.core.estimate_knowledge_score(self.agent_profiles[agent_name], topic)

    def suggest_collaborator(self, task: str) -> List[str]:
        """Suggests collaborators via Core."""
        return self.core.rank_collaborators(self.agent_profiles, task)

    def get_mental_map(self) -> Dict[str, Any]:
        """Returns the collective mental map."""
        # The core already returns serializable lists
        return self.agent_profiles
