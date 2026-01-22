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
MoE Gatekeeper (Phase 61).
Routes tasks to specialized agents (experts) based on semantic similarity.
"""

import logging
import numpy as np
import asyncio
from typing import List, Dict, Any, Optional
from src.core.base.common.models.communication_models import ExpertProfile, MoERoutingDecision
from src.infrastructure.engine.models.similarity import EmbeddingSimilarityService
from .audit_logger import SwarmAuditLogger

logger = logging.getLogger(__name__)

class MoEGatekeeper:
    """
    Orchestrates expert selection across the swarm.
    Unlike compute-level MoE, this works at the task/agent level.
    """
    
    def __init__(self, 
                 similarity_service: EmbeddingSimilarityService, 
                 audit_logger: Optional[SwarmAuditLogger] = None,
                 topology_manager: Optional[Any] = None,
                 reward_predictor: Optional[Any] = None):
        self.similarity_service = similarity_service
        self.audit_logger = audit_logger
        self.topology_manager = topology_manager
        self.reward_predictor = reward_predictor
        self.experts: Dict[str, ExpertProfile] = {}
        self.routing_cache: Dict[str, MoERoutingDecision] = {}
        self.max_cache_size = 1000

    def register_expert(self, profile: ExpertProfile):
        """Adds an expert to the routing table."""
        self.experts[profile.agent_id] = profile
        # Clear cache when expert list changes to ensure routing remains accurate
        self.routing_cache.clear()
        logger.info(f"Gatekeeper: Registered expert {profile.agent_id}. Cache cleared.")

    def update_expert_performance(self, agent_id: str, new_score: float):
        """Updates the performance score for a specific expert."""
        if agent_id in self.experts:
            self.experts[agent_id].performance_score = new_score
            # Invalidate cache as routing weights will change
            self.routing_cache.clear()
            logger.debug(f"Gatekeeper: Updated {agent_id} score to {new_score}. Cache cleared.")

    async def route_task(self, task_prompt: str, top_k: int = 2) -> MoERoutingDecision:
        """
        Calculates the best experts for a given task.
        Uses embedding similarity between the task and expert specialization vectors.
        Includes a fast-lookup cache for repeat tasks.
        """
        if not self.experts:
            raise ValueError("No experts registered in MoE Gatekeeper.")

        # Cache Lookup
        cache_key = f"{task_prompt[:128]}_{top_k}"
        if cache_key in self.routing_cache:
            logger.debug(f"Gatekeeper: Cache hit for task '{task_prompt[:20]}...'")
            return self.routing_cache[cache_key]
            
        task_emb = await self.similarity_service.get_embedding(task_prompt)
        decision = await self._compute_routing(task_prompt, task_emb, top_k)
        
        # Phase 70: Track usage for dynamic scaling/cloning
        if self.topology_manager:
            for expert_id in decision.selected_experts:
                self.topology_manager.record_usage(expert_id)

        # Cache Update
        if len(self.routing_cache) < self.max_cache_size:
            self.routing_cache[cache_key] = decision
            
        return decision

    async def batch_route_tasks(self, task_prompts: List[str], top_k: int = 2) -> List[MoERoutingDecision]:
        """
        Batches multiple routing requests to reduce embedding latency.
        """
        # In a real system, similarity_service.get_embeddings would handle batching
        # Here we simulate the parallel speedup
        tasks = [self.route_task(p, top_k) for p in task_prompts]
        return await asyncio.gather(*tasks)

    async def _compute_routing(self, prompt: str, task_emb: np.ndarray, top_k: int) -> MoERoutingDecision:
        """Internal logic for calculating weights."""
        scores = []
        agent_ids = list(self.experts.keys())
        
        for agent_id in agent_ids:
            profile = self.experts[agent_id]
            # Use specialization vector if available, otherwise fallback to domain keyword similarity simulation
            expert_vec = np.array(profile.specialization_vector)
            
            if len(expert_vec) == 0:
                # Mock a vector based on domains if empty
                # Use a specific seed based on the domain string for deterministic testing
                np.random.seed(abs(hash(" ".join(profile.domains))) % (2**32))
                expert_vec = np.random.randn(384).astype(np.float32)
                expert_vec /= np.linalg.norm(expert_vec)
                profile.specialization_vector = expert_vec.tolist()
                
            similarity = float(np.dot(task_emb, expert_vec))
            # Phase 68 fix: Ensure similarity is non-negative before multiplying by performance
            clamped_similarity = max(0.01, similarity)
            
            # Phase 74: Heterogeneous Hardware Boosting
            # Prefer hardware-accelerated experts if the task is complex/large
            hardware_multiplier = 1.0
            if profile.acceleration_type in ["fp8_bitnet", "h100_tensor"]:
                hardware_multiplier = 1.2
                
            final_score = clamped_similarity * profile.performance_score * hardware_multiplier
            
            # Phase 83: Reward Predictor Tuning (RL Feedback)
            if self.reward_predictor:
                final_score = self.reward_predictor.adjust_routing(agent_id, final_score)

            scores.append(final_score)
            
        # Convert to numpy for sorting
        scores_arr = np.array(scores)
        top_indices = np.argsort(scores_arr)[-top_k:][::-1]
        
        selected_experts = [agent_ids[i] for i in top_indices]
        weights = [float(scores_arr[i]) for i in top_indices]
        
        # Softmax weights
        exp_weights = np.exp(weights - np.max(weights))
        normalized_weights = (exp_weights / exp_weights.sum()).tolist()
        
        decision = MoERoutingDecision(
            task_id="moe_" + prompt[:16].replace(" ", "_"),
            selected_experts=selected_experts,
            routing_weights=normalized_weights
        )

        if self.audit_logger:
            self.audit_logger.log_event(
                task_id=decision.task_id,
                event_type="routing_decision",
                description=f"Routed task to {len(selected_experts)} experts",
                data={
                    "experts": selected_experts,
                    "weights": normalized_weights
                }
            )

        return decision
