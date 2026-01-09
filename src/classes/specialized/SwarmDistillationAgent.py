import json
from pathlib import Path

class SwarmDistillationAgent:
    """
    Compresses and distills knowledge from multiple specialized agents 
    into a unified "Master" context for more efficient retrieval.
    """
    def __init__(self, workspace_path) -> None:
        self.workspace_path = Path(workspace_path)
        self.master_context = {}

    def distill_agent_knowledge(self, agent_id, knowledge_data):
        """
        Extracts key insights from an agent's specialized knowledge.
        """
        # Simulated distillation: extract labels and high-level summaries
        distilled = {
            "agent": agent_id,
            "core_capability": knowledge_data.get("specialty", "general"),
            "key_patterns": list(knowledge_data.get("patterns", {}).keys())[:10],
            "metrics": knowledge_data.get("metrics", {})
        }
        
        self.master_context[agent_id] = distilled
        return distilled

    def get_unified_context(self):
        """
        Returns the distilled knowledge from all registered agents.
        """
        return {
            "swarm_intelligence_level": len(self.master_context) * 0.1,
            "distilled_indices": list(self.master_context.keys()),
            "master_map": self.master_context
        }

    def prune_master_context(self, threshold=0.5):
        """
        Removes outdated or low-importance knowledge from the master map.
        """
        initial_count = len(self.master_context)
        # Simulation: remove if 'capability_score' is low (if it existed)
        # For now, just a dummy prune to show capability
        return {"pruned_count": 0, "remaining_count": initial_count}
