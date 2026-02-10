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
Module: universal_agent
Implementation of Pillar 3: The Universal Agent Shell.
"""

from __future__ import annotations
import logging
from typing import Any, Dict
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.logic_manifest import LogicManifest

logger = logging.getLogger(__name__)

class UniversalAgent(BaseAgent):
    """
    IMPLEMENTATION OF PILLAR 3: The Universal Agent Shell.
    This agent does not have a fixed role; it dynamically adjusts its
    cognitive cores based on the Logic Manifest provided in the task.
    """

    def __init__(self, **kwargs):
        # Default manifest for a universal shell
        if "manifest" not in kwargs:
            kwargs["manifest"] = {
                "role": "universal_shell",
                "capabilities": ["dynamic_core_switching", "cort_reasoning"],
                "required_skills": ["reasoning", "orchestration"]
            }
        super().__init__(**kwargs)

    async def execute_query(self, query: str, context: Dict[str, Any] | None = None) -> Any:
        """
        Main cognitive loop for the Universal Agent.
        """
        # Phase 0: Explicit Role Loading (Pillar 5 Extension)
        if "assume role" in query.lower() or "use shard" in query.lower():
            role_match = query.lower().split("role")[-1].strip().split(" ")[0].strip(" .")
            if not role_match:
                role_match = query.lower().split("shard")[-1].strip().split(" ")[0].strip(" .")

            from src.core.base.lifecycle.manifest_repository import ManifestRepository
            repo = ManifestRepository()
            new_manifest = repo.get_manifest(role_match)
            if new_manifest:
                self.manifest = new_manifest
                logger.info(f"UniversalAgent: Successfully assumed role '{role_match}'")
                return {"status": "success", "message": f"Core reconfiguration complete. Now operating as '{role_match}'."}
            else:
                return {"status": "error", "message": f"Shard '{role_match}' not found in manifest repository."}

        logger.info("UniversalAgent: Analyzing intent for query: %s", query)

        # Phase 1: Reasoning / Intent Extraction via CoRT
        intent_analysis = await self.reasoning_core.reason(
            f"Analyze user intent and determine if this task is 'CRITICAL' (security/FS). Query: {query}"
        )

        # Phase 2: Consensus Check (Pillar 1)
        is_critical = "critical" in intent_analysis.lower() or "security" in intent_analysis.lower()

        if is_critical and hasattr(self.core, "fleet_instance"):
            fleet = self.core.fleet_instance
            if hasattr(fleet, "consensus_manager"):
                logger.info("UniversalAgent: Critical task detected. Triggering Swarm Consensus.")
                consensus_res = await fleet.consensus_manager.execute_with_consensus(query)
                if consensus_res.get("decision") == "APPROVED":
                    return consensus_res.get("winner_content")
                return {"status": "error", "reason": "consensus_rejected", "details": consensus_res}

        # Phase 2.5: Workflow Execution (Pillar 4)
        if self.manifest.flow_nodes:
            from src.core.base.lifecycle.workflow_executor import WorkflowExecutor
            executor = WorkflowExecutor(self)
            logger.info("UniversalAgent: Executing multi-node workflow.")
            return await executor.execute(self.manifest.flow_nodes, self.manifest.connectors)

        # Phase 3: Dynamic Skill/Core Loading (Pillar 3)
        if any(kw in intent_analysis.lower() for kw in ["code", "programming", "python"]):
            await self.skill_manager.load_skill("coding")
            self.manifest.role = "specialist_coder"
        elif any(kw in intent_analysis.lower() for kw in ["security", "vulnerability", "leak"]):
            await self.skill_manager.load_skill("security_audit")
            self.manifest.role = "specialist_security"

        # Phase 4: Execution via the standard task loop
        result = await self.run_task({
            "context": query,
            "metadata": context or {},
            "intent_hint": intent_analysis
        })

        # Pillar 8 Hardening: Distribute state to the swarm after task completion
        if hasattr(self.core, "fleet_instance"):
            fleet = self.core.fleet_instance
            if hasattr(fleet, "harden_agent_state"):
                state_data = {
                    "agent_id": self.id,
                    "last_query": query,
                    "last_result": str(result)[:1000],  # Truncate for efficiency
                    "memory_len": len(getattr(self.memory, "working_set", []))
                }
                asyncio.create_task(fleet.harden_agent_state(self.id, state_data))

        return result
