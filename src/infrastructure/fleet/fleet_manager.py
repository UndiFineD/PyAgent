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


"""Coordinator for deploying and aggregating results from multiple agents."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import contextlib
from pathlib import Path
from typing import Any, TYPE_CHECKING
from src.observability.structured_logger import StructuredLogger
from src.infrastructure.fleet.workflow_state import WorkflowState
from src.infrastructure.fleet.agent_registry import AgentRegistry
from src.infrastructure.fleet.orchestrator_registry import OrchestratorRegistry
from src.infrastructure.fleet.fleet_execution_core import FleetExecutionCore
from src.infrastructure.fleet.fleet_lifecycle_manager import FleetLifecycleManager
from src.infrastructure.fleet.fleet_interaction_recorder import FleetInteractionRecorder
from src.infrastructure.fleet.fleet_routing_core import FleetRoutingCore
from src.infrastructure.fleet.fleet_consensus_manager import FleetConsensusManager
from src.infrastructure.fleet.mixins.fleet_task_mixin import FleetTaskMixin
from src.infrastructure.fleet.mixins.fleet_routing_mixin import FleetRoutingMixin
from src.infrastructure.fleet.mixins.fleet_lifecycle_mixin import FleetLifecycleMixin
from src.infrastructure.fleet.mixins.fleet_lookup_mixin import FleetLookupMixin
from src.infrastructure.fleet.mixins.fleet_discovery_mixin import FleetDiscoveryMixin
from src.infrastructure.fleet.mixins.fleet_delegation_mixin import FleetDelegationMixin
from src.infrastructure.fleet.mixins.fleet_update_mixin import FleetUpdateMixin

# Type Hinting Imports (Phase 106)
if TYPE_CHECKING:
    pass

# Core Components

# Registry and Orchestrators
__version__ = VERSION

logger = StructuredLogger(__name__)


class FleetManager(
    FleetTaskMixin,
    FleetRoutingMixin,
    FleetLifecycleMixin,
    FleetLookupMixin,
    FleetDiscoveryMixin,
    FleetDelegationMixin,
    FleetUpdateMixin,
):
    """
    The central hub for the PyAgent ecosystem. Orchestrates a swarm of specialized
    agents to complete complex workflows, manages resource scaling, and ensures
    system-wide stability through various orchestrators.
    """

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)

        # New: Lazy Orchestrators (replaces ~50 direct instantiations)
        self.orchestrators = OrchestratorRegistry.get_orchestrator_map(self)

        # Load agents from registry (also lazy)
        # Pass self so agents can register utils/tools upon lazy instantiation
        self.agents = AgentRegistry.get_agent_map(
            self.workspace_root, fleet_instance=self
        )

        # Phase 320: LAN Discovery
        self.init_discovery(agent_id=f"fleet-{self.workspace_root.name}")

        # Phase 322: Autonomous Update Service (15-min cycle)
        self.init_update_service(interval_seconds=900)

        # Capability Hints for Lazy Loading (Core Agents)
        self._capability_hints = {
            "articulate": "LinguisticAgent",
            "reason": "ReasoningAgent",
            "code": "CoderAgent",
            "sql": "SqlQueryAgent",
            "git": "PullRequestAgent",
            "teleport": "ModalTeleportationOrchestrator",  # Orchestrator logic
            "byzantine_judge": "ByzantineConsensusAgent",
            "governance": "GovernanceAgent",
            "immune_system": "ImmuneSystemAgent",
            "neurosymbolic": "NeuroSymbolic",
            "morphologicalevolution": "MorphologicalEvolution",
            "signal_bus": "SignalBusOrchestrator",
            "world_model": "WorldModelAgent",
            "nas": "NetworkArchSearchAgent",
            "heartbeat": "HeartbeatOrchestrator",
            "entanglement": "EntanglementOrchestrator",
            "core_expansion": "CoreExpansionAgent",
            "temporal_shard": "TemporalShardAgent",
            "reality_anchor": "RealityAnchorAgent",
            "cognitive_borrowing": "CognitiveBorrowingOrchestrator",
            "architect": "ArchitectAgent",
            "fractal_knowledge": "FractalKnowledgeOrchestrator",
            "dependency_graph": "DependencyGraphAgent",
            "evolution_guard": "CoreEvolutionGuard",
            "explainability": "ExplainabilityAgent",
            "model_router": "RouterModelAgent",
            "search_mesh": "SemanticSearchMeshAgent",
            "policy_enforcement": "PolicyEnforcementAgent",
            "sovereignty_orchestrator": "SovereigntyOrchestrator",
            "fractal_orchestrator": "FractalOrchestrator",
            "intention_predictor": "IntentionPredictionAgent",
            "cooperative_comm": "CooperativeCommunicationAgent",
            "resource_curator": "ResourceCurationAgent",
            "resource_arbitrator": "SwarmArbitratorAgent",
            "honeypot": "HoneypotAgent",
            "consensus_orchestrator": "ConsensusOrchestrator",
            "speciation_orchestrator": "SpeciationOrchestrator",
            "speciation": "SpeciationAgent",
            "feature_store": "FeatureStoreAgent",
            "inter_fleet_identity": "InterFleetIdentityAgent",
            "inter_fleet_bridge": "InterFleetBridgeOrchestrator",
            "synthetic_data": "SyntheticDataAgent",
            "graph_relational": "GraphRelationalAgent",
            "empathy_engine": "EmpathyAgent",
            "neurosymbolic": "NeuroSymbolicAgent",
            "neuro_symbolic": "NeuroSymbolicAgent",
            "agent_identity": "IdentityAgent",
            "ethics_guardrail": "EthicsGuardrailAgent",
            "linguist": "LinguisticAgent",
            "model_forge": "ModelForgeAgent",
            "memorag": "MemoRAGAgent",
            "process_synthesizer": "ProcessSynthesizerAgent",
            "tool_synthesis": "ToolSynthesisAgent",
            "memory_replay": "MemoryReplayAgent",
            "swarm_distillation": "SwarmDistillationAgent",
            "fleet_economy": "FleetEconomyAgent",
            "swarm_visualizer": "SwarmVisualizerAgent",
            "consensus_conflict": "ConsensusConflictAgent",
            "visualizer": "VisualizerAgent",
            "fleet_deployer": "FleetDeployerAgent",
            "ui_architect": "UiArchitectAgent",
            "cloud_provider": "CloudProviderAgent",
            "legal_audit": "LegalAuditAgent",
            "memory_pruning": "MemoryPruningAgent",
            "logic_prover": "LogicProverAgent",
            "reward_model": "RewardModelAgent",
            "audio_reasoning": "AudioReasoningAgent",
            "entropy_guard": "EntropyGuardAgent",
            "compliance_agent": "ComplianceAgent",
            "sql_coder_agent": "SQLCoderAgent",
            "telemetry_agent": "TelemetryAgent",
            "workflow_agent": "WorkflowAgent",
        }

        self.remote_nodes: list[str] = []
        self.state: WorkflowState | None = None
        self.action_history: list[str] = []  # For loop detection
        self.kill_switch = False  # Emergency termination

        # Phase 260: Preemption
        self.active_tasks: dict[str, Any] = {}  # task_id -> {priority, agent_instances}

        # Delegated Managers (Phase 120 Extraction)
        self.execution_core = FleetExecutionCore(self)
        self.lifecycle_manager = FleetLifecycleManager(self)
        self.interaction_recorder = FleetInteractionRecorder(self)
        self.routing_core = FleetRoutingCore(self)
        self.consensus_manager = FleetConsensusManager(self)

        # Phase 123: Start Peer Discovery
        with contextlib.suppress(Exception):
            _ = self.orchestrators.discovery

    # Logic delegated to mixins

if __name__ == "__main__":
    # Test script for FleetManager
    logging.basicConfig(level=logging.INFO)
    root = Path(str(Path(__file__).resolve().parents[3]) + "")
    fleet = FleetManager(str(root))

    # These agents are used for the demo below
    from src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent
    from src.logic.agents.development.security_guard_agent import SecurityGuardAgent

    fleet.register_agent(
        "Knowledge",
        KnowledgeAgent,
        str(root / "src\logic\agents\cognitive\knowledge_agent.py"),
    )
    fleet.register_agent(
        "Security",
        SecurityGuardAgent,
        str(root / "src\logic\agents\development\security_guard_agent.py"),
    )

    workflow = [
        {"agent": "Knowledge", "action": "scan_workspace", "args": ["KnowledgeAgent"]},
        {
            "agent": "Security",
            "action": "improve_content",
            "args": ["password = os.environ.get('DB_PASSWORD')"],
        },
    ]

    # report = fleet.execute_workflow("Initial Audit", workflow) # Async call, requires await or asyncio.run
    # For now, just logging calls replacement
    logger.info("FleetManager demo execution started")
    # print(report)
    # print("\nTelemetry Summary:")
    # print(json.dumps(fleet.telemetry.get_summary(), indent=2))
    if hasattr(fleet, "telemetry"):
        logger.info("Telemetry Summary", summary=fleet.telemetry.get_summary())
