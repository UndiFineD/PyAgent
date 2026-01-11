import time
from typing import Dict, List, Any
from src.core.base.BaseAgent import BaseAgent

class StrategicPlanningAgent(BaseAgent):
    """
    Strategic Planning Agent: Handles long-term goal setting, roadmap 
    prioritization, and autonomous project management for the fleet.
    """
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.goals = []
        self.roadmap = []
        self.status_reports = []

    def set_long_term_goal(self, goal_description: str, target_date: str) -> Dict[str, Any]:
        """Adds a long-term goal for the fleet to achieve."""
        goal = {
            "id": f"GOAL-{len(self.goals) + 1}",
            "description": goal_description,
            "target_date": target_date,
            "status": "In Progress",
            "milestones": []
        }
        self.goals.append(goal)
        print(f"Strategy: Goal set - {goal_description}")
        return goal

    def add_milestone_to_goal(self, goal_id: str, milestone_description: str) -> bool:
        """Adds a specific milestone to an existing goal."""
        for goal in self.goals:
            if goal['id'] == goal_id:
                goal['milestones'].append({
                    "description": milestone_description,
                    "achieved": False
                })
                print(f"Strategy: Milestone added to {goal_id} - {milestone_description}")
                return True
        return False

    def generate_roadmap(self) -> List[Dict[str, Any]]:
        """Generates a high-level roadmap based on active goals and their milestones."""
        self.roadmap = []
        for goal in self.goals:
            self.roadmap.append({
                "goal": goal['description'],
                "completion": self._calculate_completion(goal),
                "milestones_count": len(goal['milestones'])
            })
        return self.roadmap

    def _calculate_completion(self, goal: Dict[str, Any]) -> float:
        """Calculates completion percentage based on achieved milestones."""
        if not goal['milestones']:
            return 0.0
        achieved = sum(1 for m in goal['milestones'] if m['achieved'])
        return (achieved / len(goal['milestones'])) * 100

    def mark_milestone_complete(self, goal_id: str, milestone_description: str) -> bool:
        """Marks a milestone as achieved."""
        for goal in self.goals:
            if goal['id'] == goal_id:
                for milestone in goal['milestones']:
                    if milestone['description'] == milestone_description:
                        milestone['achieved'] = True
                        print(f"Strategy: Milestone '{milestone_description}' achieved for {goal_id}!")
                        return True
        return False

    def get_strategic_summary(self) -> Dict[str, Any]:
        """Provides a summary of strategic alignment and progress."""
        return {
            "active_goals": len(self.goals),
            "roadmap_items": len(self.generate_roadmap()),
            "overall_health": "On Track" if all(self._calculate_completion(g) >= 0 for g in self.goals) else "At Risk"
        }
