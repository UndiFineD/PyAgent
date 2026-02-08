# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\eval.py\tasks.py\default_task_d7a95466cd87.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\eval\tasks\default_task.py

from typing import Any, Dict, List, Optional

from fle.agents import TaskResponse

from fle.env import FactorioInstance

from fle.eval.tasks import TaskABC


class DefaultTask(TaskABC):
    def __init__(
        self,
        trajectory_length,
        goal_description: str,
        task_key: str,
        agent_instructions: Optional[List[str]] = None,
    ):
        super().__init__(
            trajectory_length,
            starting_inventory={},
            goal_description=goal_description,
            task_key=task_key,
            all_technology_reserached=False,
            agent_instructions=agent_instructions,
        )

        self.starting_game_state = None

    def verify(self, score: float, instance: FactorioInstance, step_statistics: Dict) -> TaskResponse:
        return TaskResponse(success=False, meta={})

    def _to_dict(self) -> Dict[str, Any]:
        return {
            "goal_description": self.goal_description,
            "trajectory_length": self.trajectory_length,
            "starting_inventory": self.starting_inventory,
            "initial_state": (self.starting_game_state.to_raw() if self.starting_game_state else None),
        }

    def setup_instance(self, instance):
        """Code to provision the task environment"""

        pass
