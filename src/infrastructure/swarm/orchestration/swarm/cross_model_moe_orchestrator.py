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
Cross-Model MoE Orchestrator (Phase 61).
Manages task lifecycle across multiple specialized agents.
"""

<<<<<<< HEAD
import asyncio
import logging
from typing import Any, Dict, Optional

from src.infrastructure.swarm.orchestration.swarm.expert_fusion import \
    WeightedExpertFusion
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import \
    MoEGatekeeper

logger = logging.getLogger(__name__)


=======
import logging
import asyncio
from typing import List, Dict, Any, Optional
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.infrastructure.swarm.orchestration.swarm.expert_fusion import WeightedExpertFusion
from src.core.base.common.models.communication_models import MoERoutingDecision

logger = logging.getLogger(__name__)

>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class CrossModelMoEOrchestrator:
    """
    Swarm-level Mixture of Experts.
    Turns the entire agent fleet into a distributed MoE.
    """
<<<<<<< HEAD

    def __init__(self, gatekeeper: MoEGatekeeper, fusion_engine: Optional[WeightedExpertFusion] = None) -> None:
        self.gatekeeper = gatekeeper
        self.fusion_engine = fusion_engine or WeightedExpertFusion()
        self.agent_registry: Dict[str, Any] = {}  # Map of agent_id to actual agent instances/stubs
        self.expert_health: Dict[str, bool] = {}  # agent_id to is_healthy
=======
    
    def __init__(self, gatekeeper: MoEGatekeeper, fusion_engine: Optional[WeightedExpertFusion] = None):
        self.gatekeeper = gatekeeper
        self.fusion_engine = fusion_engine or WeightedExpertFusion()
        self.agent_registry: Dict[str, Any] = {} # Map of agent_id to actual agent instances/stubs
        self.expert_health: Dict[str, bool] = {} # agent_id to is_healthy
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.timeout_sec = 10.0

    def register_agent_instance(self, agent_id: str, instance: Any):
        """Link an expert ID to a runnable agent instance."""
        self.agent_registry[agent_id] = instance
        self.expert_health[agent_id] = True

    async def execute_moe_task(self, task: str, mode: str = "best_expert") -> Any:
        """
        Routes and executes a task using the MoE pattern.
        Includes self-healing logic (Phase 66) to handle expert failures.
        """
        logger.info(f"MoE Orchestrator: Routing task '{task[:50]}...'")
<<<<<<< HEAD

        # 1. Routing
        decision = await self.gatekeeper.route_task(task, top_k=2)

        if not decision.selected_experts:
            raise RuntimeError("MoE Routing failed: No experts selected.")

        logger.info(f"MoE Orchestrator: Selected experts {decision.selected_experts}")

=======
        
        # 1. Routing
        decision = await self.gatekeeper.route_task(task, top_k=2)
        
        if not decision.selected_experts:
            raise RuntimeError("MoE Routing failed: No experts selected.")
            
        logger.info(f"MoE Orchestrator: Selected experts {decision.selected_experts}")
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # 2. Execution with Self-Healing
        if mode == "best_expert":
            for expert_id in decision.selected_experts:
                if not self.expert_health.get(expert_id, True):
                    continue
<<<<<<< HEAD

                expert_agent = self.agent_registry.get(expert_id)
                if not expert_agent:
                    continue

                try:
                    logger.info(f"MoE Orchestrator: Attempting Expert: {expert_id}")
                    return await asyncio.wait_for(expert_agent.process_request(task), timeout=self.timeout_sec)
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    logger.warning(f"MoE Orchestrator: Expert {expert_id} failed: {e}. Re-routing...")
                    self.expert_health[expert_id] = False  # Mark as unhealthy
                    # The loop will naturally try the next expert in 'selected_experts'

            raise RuntimeError("MoE Self-Healing: All selected experts failed or are unreachable.")

=======
                    
                expert_agent = self.agent_registry.get(expert_id)
                if not expert_agent:
                    continue
                
                try:
                    logger.info(f"MoE Orchestrator: Attempting Expert: {expert_id}")
                    return await asyncio.wait_for(expert_agent.process_request(task), timeout=self.timeout_sec)
                except (asyncio.TimeoutError, Exception) as e:
                    logger.warning(f"MoE Orchestrator: Expert {expert_id} failed: {e}. Re-routing...")
                    self.expert_health[expert_id] = False # Mark as unhealthy
                    # The loop will naturally try the next expert in 'selected_experts'
            
            raise RuntimeError("MoE Self-Healing: All selected experts failed or are unreachable.")
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        elif mode == "mixture":
            # Concurrent execution on multiple experts
            # Phase 66 updates: handle partial failures in mixture
            pending_tasks = []
<<<<<<< HEAD

=======
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            for i, expert_id in enumerate(decision.selected_experts):
                if not self.expert_health.get(expert_id, True):
                    continue
                agent = self.agent_registry.get(expert_id)
                if agent:
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                    async def safe_exec(aid, a, w):
                        try:
                            res = await asyncio.wait_for(a.process_request(task), timeout=self.timeout_sec)
                            return (True, aid, w, res)
<<<<<<< HEAD
                        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
=======
                        except Exception as e:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                            logger.error(f"MoE Mixture: {aid} failed: {e}")
                            self.expert_health[aid] = False
                            return (False, aid, w, None)

                    pending_tasks.append(safe_exec(expert_id, agent, decision.routing_weights[i]))
<<<<<<< HEAD

            if not pending_tasks:
                raise RuntimeError("MoE Mixture failed: No healthy expert agents available.")

            raw_results = await asyncio.gather(*pending_tasks)

=======
            
            if not pending_tasks:
                raise RuntimeError("MoE Mixture failed: No healthy expert agents available.")
                
            raw_results = await asyncio.gather(*pending_tasks)
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            # Filter successful ones
            final_results = []
            final_weights = []
            final_experts = []
            for success, eid, w, res in raw_results:
                if success:
                    final_results.append(res)
                    final_weights.append(w)
                    final_experts.append(eid)

            if not final_results:
                raise RuntimeError("MoE Mixture: All parallel experts failed.")
<<<<<<< HEAD

            # 3. Fusion / Consensus
            fusion_res = await self.fusion_engine.fuse_outputs(
                outputs=final_results, weights=final_weights, expert_ids=final_experts, mode="weighted_plurality"
            )

            logger.info(
                f"MoE Orchestrator: Fused {len(final_results)} outputs with consensus {fusion_res.consensus_score}"
            )
            return fusion_res.merged_content

=======
            
            # 3. Fusion / Consensus
            fusion_res = await self.fusion_engine.fuse_outputs(
                outputs=final_results,
                weights=final_weights,
                expert_ids=final_experts,
                mode="weighted_plurality"
            )
            
            logger.info(f"MoE Orchestrator: Fused {len(final_results)} outputs with consensus {fusion_res.consensus_score}")
            return fusion_res.merged_content
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return None
