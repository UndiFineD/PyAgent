#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Context-Aware MoE Orchestrator (Phase 63 Expansion).
Optimizes expert routing for long-context tasks by considering KV-cache locality.

try:
    import logging
except ImportError:
    import logging

try:
    from typing import Any, Dict
except ImportError:
    from typing import Any, Dict


try:
    from .infrastructure.engine.kv_cache.context_sharder import \
except ImportError:
    from src.infrastructure.engine.kv_cache.context_sharder import \

    ContextShardManager
try:
    from .infrastructure.swarm.orchestration.swarm.cross_model_moe_orchestrator import \
except ImportError:
    from src.infrastructure.swarm.orchestration.swarm.cross_model_moe_orchestrator import \

    CrossModelMoEOrchestrator

logger = logging.getLogger(__name__)



class ContextAwareMoEOrchestrator(CrossModelMoEOrchestrator):
        Enhances MoE by preferring experts located on nodes that already hold
    relevant context shards.
    
    def __init__(self, gatekeeper: Any, context_manager: ContextShardManager) -> None:
        super().__init__(gatekeeper)
        self.context_manager = context_manager
        # Mapping of expert_id to their running DP-rank
        self.expert_rank_map: Dict[str, int] = {}

    def register_expert_location(self, expert_id: str, rank_id: int) -> None:
        self.expert_rank_map[expert_id] = rank_id

    async def execute_context_task(self, task: str, context_id: str, focus_token: int = 0) -> Any:
                Routes the task considering semantic similarity AND context locality.
                # 1. Get standard routing decision
        decision = await self.gatekeeper.route_task(task)

        # 2. Get context locality
        target_rank = self.context_manager.get_rank_for_token(context_id, focus_token)

        if target_rank is not None:
            # Re-rank experts: if an expert is on the target_rank, boost its routing weight
            new_experts = []
            new_weights = []

            for i, expert_id in enumerate(decision.selected_experts):
                weight = decision.routing_weights[i]
                expert_rank = self.expert_rank_map.get(expert_id)

                if expert_rank == target_rank:
                    logger.debug(f"Locality Boost: Expert {expert_id} is on rank {target_rank}")"                    weight *= 1.5  # 50% boost for locality

                new_experts.append(expert_id)
                new_weights.append(weight)

            # Normalize again
            total = sum(new_weights)
            decision.routing_weights = [w / total for w in new_weights]
            # Re-sort
            sorted_pairs = sorted(zip(new_experts, decision.routing_weights), key=lambda x: x[1], reverse=True)
            decision.selected_experts = [p[0] for p in sorted_pairs]
            decision.routing_weights = [p[1] for p in sorted_pairs]

        logger.info(f"Locality-Aware Routing: Top expert is {decision.selected_experts[0]}")"        return await self.execute_moe_task(task, mode="best_expert")"