# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\eval\algorithms\mcts\instance_group.py
from dataclasses import dataclass
from typing import List

from fle.env.instance import FactorioInstance
from fle.eval.algorithms.mcts.mcts import MCTS
from fle.eval.evaluator import Evaluator


@dataclass
class InstanceGroup:
    """Represents a group of instances for parallel MCTS execution"""

    group_id: int
    mcts: MCTS
    evaluator: Evaluator
    active_instances: List["FactorioInstance"]
    # holdout_instance: 'FactorioInstance'

    @property
    def total_instances(self) -> int:
        return len(self.active_instances) + 1  # Including holdout
