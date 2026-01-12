import json
from pathlib import Path
from typing import Dict, List, Any
from src.logic.agents.swarm.core.LessonCore import LessonCore, Lesson

class SwarmDistillationAgent:
    """
    Compresses and distills knowledge from multiple specialized agents 
    into a unified "Master" context for more efficient retrieval.
    Integrated with LessonCore for failure mode propagation.
    """
    def __init__(self, workspace_path) -> None:
        self.workspace_path = Path(workspace_path)
        self.master_context = {}
        self.lesson_core = LessonCore()
        self.lessons: List[Lesson] = []

    def distill_agent_knowledge(self, agent_id, knowledge_data) -> Dict[str, Any]:
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

    def register_failure_lesson(self, error: str, cause: str, fix: str) -> str:
        """Registers a failure mode and its resolution logic."""
        lesson = Lesson(error_pattern=error, cause=cause, solution=fix)
        f_hash = self.lesson_core.record_lesson(lesson)
        self.lessons.append(lesson)
        return f_hash

    def check_for_prior_art(self, error_msg: str) -> List[Dict[str, Any]]:
        """Checks if any other agent has already solved this error."""
        related = self.lesson_core.get_related_lessons(error_msg, self.lessons)
        return [{"cause": l.cause, "solution": l.solution} for l in related]

    def get_unified_context(self) -> Dict[str, Any]:
        """
        Returns the distilled knowledge from all registered agents.
        """
        return {
            "swarm_intelligence_level": len(self.master_context) * 0.1,
            "distilled_indices": list(self.master_context.keys()),
            "master_map": self.master_context
        }

    def prune_master_context(self, threshold=0.5) -> Dict[str, Any]:
        """
        Removes outdated or low-importance knowledge from the master map.
        """
        initial_count = len(self.master_context)
        # Simulation: remove if 'capability_score' is low (if it existed)
        # For now, just a dummy prune to show capability
        return {"pruned_count": 0, "remaining_count": initial_count}
