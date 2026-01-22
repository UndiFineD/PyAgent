#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Expert Specialization Evolution (Phase 68).
Reinforcement loop that adjusts expert scores based on real-world outcomes.
"""

import logging
<<<<<<< HEAD
from typing import List

from src.core.base.common.models.communication_models import ExpertEvaluation
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import \
    MoEGatekeeper

logger = logging.getLogger(__name__)


=======
from typing import Dict, List
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.core.base.common.models.communication_models import ExpertEvaluation

logger = logging.getLogger(__name__)

>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class ExpertEvolutionService:
    """
    Analyzes expert evaluations and refines the routing scores in the Gatekeeper.
    Uses an exponential moving average (EMA) to prevent over-reacting to single failures.
    """
<<<<<<< HEAD

    def __init__(self, gatekeeper: MoEGatekeeper, learning_rate: float = 0.1) -> None:
=======
    
    def __init__(self, gatekeeper: MoEGatekeeper, learning_rate: float = 0.1):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.gatekeeper = gatekeeper
        self.learning_rate = learning_rate
        # History of evaluations for tracking
        self.evaluation_history: List[ExpertEvaluation] = []

    def process_evaluation(self, evaluation: ExpertEvaluation):
        """
        Ingests feedback and updates the expert's performance score.
        """
        self.evaluation_history.append(evaluation)
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        expert_id = evaluation.expert_id
        current_profile = self.gatekeeper.experts.get(expert_id)
        if not current_profile:
            logger.warning(f"Evolution: Received evaluation for unknown expert {expert_id}")
            return
<<<<<<< HEAD

        current_score = current_profile.performance_score

        # Calculate target score (weighted by quality and correctness)
        target_score = evaluation.quality_score if evaluation.is_correct else (evaluation.quality_score * 0.5)

        # EMA update: score = (1 - alpha) * current + alpha * target
        new_score = ((1.0 - self.learning_rate) * current_score) + (self.learning_rate * target_score)

        # Clamping
        new_score = max(0.1, min(1.0, new_score))

=======
            
        current_score = current_profile.performance_score
        
        # Calculate target score (weighted by quality and correctness)
        target_score = evaluation.quality_score if evaluation.is_correct else (evaluation.quality_score * 0.5)
        
        # EMA update: score = (1 - alpha) * current + alpha * target
        new_score = ((1.0 - self.learning_rate) * current_score) + (self.learning_rate * target_score)
        
        # Clamping
        new_score = max(0.1, min(1.0, new_score))
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.gatekeeper.update_expert_performance(expert_id, new_score)
        logger.info(f"Evolution: Expert {expert_id} evolved: {current_score:.3f} -> {new_score:.3f}")

    def get_top_performing_experts(self, limit: int = 5) -> List[str]:
        """Returns the IDs of the highest scoring experts."""
<<<<<<< HEAD
        sorted_experts = sorted(self.gatekeeper.experts.values(), key=lambda x: x.performance_score, reverse=True)
=======
        sorted_experts = sorted(
            self.gatekeeper.experts.values(), 
            key=lambda x: x.performance_score, 
            reverse=True
        )
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return [e.agent_id for e in sorted_experts[:limit]]
