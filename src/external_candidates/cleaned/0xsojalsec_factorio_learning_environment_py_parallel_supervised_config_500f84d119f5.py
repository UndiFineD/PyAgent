# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\eval.py\algorithms.py\mcts.py\parallel_supervised_config_500f84d119f5.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\eval\algorithms\mcts\parallel_supervised_config.py

from typing import Any, Dict

from fle.commons.models.game_state import GameState


class SupervisedExecutorConfig:
    """Configuration for ParallelMCTS"""

    def __init__(
        self,
        n_parallel: int,
        model_to_evaluate: str,
        supervised_kwargs: Dict[str, Any] = None,
        initial_state: GameState = None,
    ):
        self.n_parallel = n_parallel

        self.model_to_evaluate = model_to_evaluate

        self.supervised_kwargs = supervised_kwargs or {}

        self.initial_state = initial_state

    def _to_dict(self) -> Dict[str, Any]:
        return {
            "n_parallel": self.n_parallel,
            "model_to_evaluate": self.model_to_evaluate,
            "supervised_kwargs": self.supervised_kwargs,
            "initial_state": (self.initial_state.to_raw() if self.initial_state else None),
        }
