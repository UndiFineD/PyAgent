# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\gym_env.py\action_bb3cf1c7e8bd.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\gym_env\action.py

from dataclasses import dataclass

from typing import Any, Dict, Optional

from fle.commons.models.game_state import GameState


@dataclass
class Action:
    """Action for the Factorio gym environment"""

    code: str

    agent_idx: int = 0

    game_state: Optional[GameState] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert action to dictionary format expected by the environment"""

        return {
            "code": self.code,
            "agent_idx": self.agent_idx,
            "game_state": self.game_state.to_raw() if self.game_state else None,
        }
