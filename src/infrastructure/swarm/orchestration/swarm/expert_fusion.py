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
Weighted Expert Fusion (Phase 62).
Provides consensus mechanisms to merge outputs from multiple experts in an MoE swarm.
"""

import logging
<<<<<<< HEAD
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np

from src.infrastructure.swarm.orchestration.swarm.audit_logger import SwarmAuditLogger

logger = logging.getLogger(__name__)


@dataclass
class FusionResult:
    """The result of a weighted expert fusion operation."""

=======
import asyncio
from typing import List, Dict, Any, Union, Optional
from dataclasses import dataclass
from collections import Counter
from .audit_logger import SwarmAuditLogger

logger = logging.getLogger(__name__)

@dataclass
class FusionResult:
    """The result of a weighted expert fusion operation."""
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    merged_content: str
    consensus_score: float
    contributing_experts: List[str]
    metadata: Dict[str, Any]

<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class WeightedExpertFusion:
    """
    Handles merging of agent outputs using various consensus strategies.
    Supported strategies:
    - 'weighted_plurality': Most common result weighted by expert performance.
    - 'consensus_ranking': Uses embedding similarity to find the most 'central' answer.
    - 'hierarchical_edit': Merges text segments (future integration for token-level).
    """

<<<<<<< HEAD
    def __init__(self, similarity_service: Any = None, audit_logger: Optional[SwarmAuditLogger] = None) -> None:
=======
    def __init__(self, similarity_service: Any = None, audit_logger: Optional[SwarmAuditLogger] = None):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.similarity_service = similarity_service
        self.audit_logger = audit_logger

    async def fuse_outputs(
<<<<<<< HEAD
        self,
        outputs: List[str],
        weights: List[float],
        expert_ids: List[str],
        mode: str = "weighted_plurality",
        task_id: Optional[str] = None,
=======
        self, 
        outputs: List[str], 
        weights: List[float], 
        expert_ids: List[str],
        mode: str = "weighted_plurality",
        task_id: Optional[str] = None
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    ) -> FusionResult:
        """
        Main fusion entry point.
        """
        if not outputs or len(outputs) != len(weights):
            raise ValueError("Outputs and weights must be non-empty and of equal length.")

        if mode == "weighted_plurality":
            result = await self._weighted_plurality(outputs, weights, expert_ids)
        elif mode == "semantic_consensus":
            result = await self._semantic_consensus(outputs, weights, expert_ids)
        else:
            # Fallback to top expert
            result = FusionResult(
                merged_content=outputs[0],
                consensus_score=weights[0],
                contributing_experts=[expert_ids[0]],
<<<<<<< HEAD
                metadata={"mode": "fallback_top_1"},
=======
                metadata={"mode": "fallback_top_1"}
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            )

        if self.audit_logger and task_id:
            self.audit_logger.log_event(
                task_id=task_id,
                event_type="expert_fusion",
                description=f"Merged expert results using {mode}",
<<<<<<< HEAD
                data={"consensus_score": result.consensus_score, "experts": result.contributing_experts, "mode": mode},
=======
                data={
                    "consensus_score": result.consensus_score,
                    "experts": result.contributing_experts,
                    "mode": mode
                }
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            )

        return result

    async def _weighted_plurality(
<<<<<<< HEAD
        self, outputs: List[str], weights: List[float], expert_ids: List[str]
=======
        self, 
        outputs: List[str], 
        weights: List[float], 
        expert_ids: List[str]
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    ) -> FusionResult:
        """
        Classic majority-vote weighted by expert scores.
        """
        scores = {}
        for out, weight in zip(outputs, weights):
            scores[out] = scores.get(out, 0.0) + weight
<<<<<<< HEAD

        best_output = max(scores, key=scores.get)
        total_weight = sum(weights)
        consensus_score = scores[best_output] / total_weight if total_weight > 0 else 0

=======
            
        best_output = max(scores, key=scores.get)
        total_weight = sum(weights)
        consensus_score = scores[best_output] / total_weight if total_weight > 0 else 0
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return FusionResult(
            merged_content=best_output,
            consensus_score=consensus_score,
            contributing_experts=expert_ids,
<<<<<<< HEAD
            metadata={"strategy": "weighted_plurality", "vote_distribution": scores},
        )

    async def _semantic_consensus(
        self, outputs: List[str], weights: List[float], expert_ids: List[str]
=======
            metadata={"strategy": "weighted_plurality", "vote_distribution": scores}
        )

    async def _semantic_consensus(
        self, 
        outputs: List[str], 
        weights: List[float], 
        expert_ids: List[str]
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    ) -> FusionResult:
        """
        Finds the answer that is semantically closest to all other weighted answers.
        Requires SimilarityService.
        """
        if not self.similarity_service:
            # Fallback to weighted plurality if no similarity service
            return await self._weighted_plurality(outputs, weights, expert_ids)
<<<<<<< HEAD

=======
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Calculate similarity matrix (Simplified for Phase 62)
        mean_scores = []
        for i, anchor in enumerate(outputs):
            sims = await self.similarity_service.batch_similarity(anchor, outputs)
            weighted_sim = sum(s * w for s, w in zip(sims, weights))
            mean_scores.append(weighted_sim)
<<<<<<< HEAD

        best_idx = int(np.argmax(mean_scores))

=======
            
        best_idx = int(np.argmax(mean_scores))
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return FusionResult(
            merged_content=outputs[best_idx],
            consensus_score=float(mean_scores[best_idx]),
            contributing_experts=expert_ids,
<<<<<<< HEAD
            metadata={"strategy": "semantic_consensus", "best_index": best_idx},
=======
            metadata={"strategy": "semantic_consensus", "best_index": best_idx}
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        )
