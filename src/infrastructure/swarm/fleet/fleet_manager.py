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

import asyncio
import contextlib
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.manifest_repository import ManifestRepository
from src.infrastructure.swarm.resilience.distributed_backup import DistributedBackup
from src.maintenance.evolution.code_improver import EvolutionLoop
from src.infrastructure.swarm.fleet.agent_registry import AgentRegistry
from src.infrastructure.swarm.fleet.fleet_consensus_manager import \
    FleetConsensusManager
from src.infrastructure.swarm.fleet.fleet_execution_core import \
    FleetExecutionCore
from src.infrastructure.swarm.fleet.fleet_interaction_recorder import \
    FleetInteractionRecorder
from src.infrastructure.swarm.fleet.fleet_lifecycle_manager import \
    FleetLifecycleManager
from src.infrastructure.swarm.fleet.fleet_routing_core import FleetRoutingCore
from src.infrastructure.swarm.fleet.resource_monitor import ResourceMonitor
from src.infrastructure.swarm.voyager.transport_layer import VoyagerTransport
from src.infrastructure.swarm.voyager.discovery_node import DiscoveryNode
from src.infrastructure.swarm.fleet.mixins.fleet_backup_mixin import \
    FleetBackupMixin
from src.infrastructure.swarm.fleet.mixins.fleet_delegation_mixin import \
    FleetDelegationMixin
from src.infrastructure.swarm.fleet.mixins.fleet_discovery_mixin import \
    FleetDiscoveryMixin
from src.infrastructure.swarm.fleet.mixins.fleet_lifecycle_mixin import \
    FleetLifecycleMixin
from src.infrastructure.swarm.fleet.mixins.fleet_lookup_mixin import \
    FleetLookupMixin
from src.infrastructure.swarm.fleet.mixins.fleet_routing_mixin import \
    FleetRoutingMixin
from src.infrastructure.swarm.fleet.mixins.fleet_task_mixin import \
    FleetTaskMixin
from src.infrastructure.swarm.fleet.mixins.fleet_update_mixin import \
    FleetUpdateMixin
from src.infrastructure.swarm.fleet.orchestrator_registry import \
    OrchestratorRegistry
from src.infrastructure.swarm.fleet.workflow_state import WorkflowState
from src.observability.structured_logger import StructuredLogger
from src.infrastructure.swarm.topology_reporter import SwarmTopologyReporter
from src.infrastructure.security.firewall.zero_trust import ZeroTrustFirewall

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
    FleetBackupMixin,
):  # pylint: disable=too-many-ancestors
    """
    The central hub for the PyAgent ecosystem. Orchestrates a swarm of specialized
    agents to complete complex workflows, manages resource scaling, and ensures
    system-wide stability through various orchestrators.
    """

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.manifest_repo = ManifestRepository()
        self.backup_node = DistributedBackup(node_id=f"node-{self.workspace_root.name}")
        self.evolution_loop = EvolutionLoop(self)
        self.topology_reporter = SwarmTopologyReporter(
            output_path=str(self.workspace_root / "data" / "logs" / "topology.json")
        )

        # Phase 324: Zero-Trust Security (Pillar 7)
        self.firewall = ZeroTrustFirewall(owner_key=f"node-key-{self.workspace_root.name}")

        # New: Lazy Orchestrators (replaces ~50 direct instantiations)
        self.orchestrators = OrchestratorRegistry.get_orchestrator_map(self)

        # Load agents from registry (also lazy)
        # Pass self so agents can register utils/tools upon lazy instantiation
        self.agents = AgentRegistry.get_agent_map(self.workspace_root, fleet_instance=self)

        # Phase 320: LAN Discovery
        self.init_discovery(agent_id=f"fleet-{self.workspace_root.name}")

        # Phase 319-320: Voyager P2P Transport & Discovery
        self.voyager_transport = VoyagerTransport()
        self.voyager_discovery = DiscoveryNode(node_name=f"Fleet-{self.workspace_root.name}")
        
        # Start voyager services (async)
        asyncio.create_task(self.voyager_transport.start_server(self._handle_voyager_message))
        asyncio.create_task(self.voyager_discovery.start_advertising())
        asyncio.create_task(self.voyager_discovery.start_discovery())

        # Phase 320: Resource Monitoring & Autonomous Balancing
        self.resource_monitor = ResourceMonitor()
        asyncio.create_task(self.resource_monitor.start())
        asyncio.create_task(self.evolution_loop.start())
        asyncio.create_task(self._topology_loop())

        # Phase 322: Autonomous Update Service (15-min cycle)
        self.init_update_service(interval_seconds=900)

        # Capability Hints for Lazy Loading (Core Agents)
        self.capability_hints = {
            "articulate": "LinguisticAgent",
            "reason": "ReasoningAgent",
            "code": "CoderAgent",
            "sql": "SqlQueryAgent",
            "git": "PullRequestAgent",
            "teleport": "ModalTeleportationOrchestrator",  # Orchestrator logic
            "byzantine_judge": "ByzantineConsensusAgent",
            "governance": "GovernanceAgent",
            "immune_system": "ImmuneSystemAgent",
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
            "ui_architect": "UiArchitectAgent",
            "evolution_guard": "CoreEvolutionGuard",
            "explainability": "ExplainabilityAgent",
            "Explainability": "ExplainabilityAgent",
            "privacy_guard": "PrivacyGuardAgent",
            "PrivacyGuard": "PrivacyGuardAgent",
            "security_audit": "SecurityAuditAgent",
            "SecurityAudit": "SecurityAuditAgent",
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
            "universal": "UniversalAgent",
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

    async def handle_user_command(self, command: str) -> Dict[str, Any]:
        """Entry point for the Universal Agent Shell (Pillar 3)."""
        logger.info(f"FleetManager: Received user command: {command}")
        
        # 1. Record user input in reasoning chain
        self.interaction_recorder.record_interaction(
            user_input=command,
            agent_id="User",
            role="user"
        )
        
        # 2. Utilize the Universal Agent for Pillar 3 execution
        try:
            # Check for UniversalAgent in registry
            if "UniversalAgent" not in self.agents:
                from src.logic.agents.system.universal_agent import UniversalAgent
                self.register_agent(
                    "UniversalAgent", 
                    UniversalAgent, 
                    str(self.workspace_root / "src" / "logic" / "agents" / "system" / "universal_agent.py")
                )

            agent = self.agents["UniversalAgent"]
            logger.info("FleetManager: Dispatched to UniversalAgent (Pillar 3)")
            
            # Execute via the Universal Shell
            result = await agent.execute_query(command)
            
            # 3. Record response
            self.interaction_recorder.record_interaction(
                user_input=command,
                agent_id="UniversalAgent",
                role="assistant",
                content=str(result)
            )
            return {"status": "success", "agent": "UniversalAgent", "result": result}
            
        except Exception as e:
            logger.error(f"FleetManager: UniversalAgent failed: {e}")
            # Fallback to standard delegation for security/reasons
            target_agent = "ReasoningAgent"
            if "code" in command.lower() or "fix" in command.lower():
                target_agent = "CoderAgent"
            
            try:
                result = await self.delegate_to(target_agent, command)
                return {"status": "success", "agent": target_agent, "result": result}
            except Exception as e2:
                return {"status": "error", "message": str(e2)}

    # Logic delegated to mixins

    async def _handle_voyager_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handles incoming P2P messages from the Voyager transport layer."""
        # Phase 324: Zero-Trust Validation (Pillar 7)
        signature = message.get("signature", "unsigned")
        sender_id = message.get("sender_id", "unknown")
        
        if not self.firewall.validate_message(message, signature, sender_id):
            logger.warning(f"FleetManager: Blocked message from {sender_id} - Zero-Trust Violation")
            return {"status": "error", "reason": "security_violation"}

        msg_type = message.get("type")

        if msg_type == "delegate_task":
            agent_type = message.get("agent_type")
            prompt = message.get("prompt")
            try:
                result = await self.delegate_to(agent_type, prompt)
                return {"status": "success", "result": result}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        elif msg_type == "resource_status":
            return {"status": "ok"}

        elif msg_type == "shard_store" or msg_type == "store_shard":
            shard = message.get("shard", {})
            success = self.backup_node.store_shard_locally(shard)
            return {"status": "success" if success else "error"}

        elif msg_type == "shard_request" or msg_type == "request_shard":
            state_hash = message.get("hash")
            shards = self.backup_node.get_local_shards_for_hash(state_hash)
            return {"status": "success", "shards": shards}

        return {"status": "unknown_message_type"}

    async def _topology_loop(self) -> None:
        """Periodically refreshes the swarm topology visualization data (Pillar 9)."""
        while True:
            try:
                # Reset snapshot lists
                self.topology_reporter.nodes = []
                self.topology_reporter.links = []

                # 1. Self node with Resource metrics
                stats = self.resource_monitor.get_latest_stats()
                self.topology_reporter.update_traffic("localhost", stats.get("network_io", {}).get("bytes_sent", 0))
                
                self.topology_reporter.record_node(
                    node_id="localhost",
                    group="gateway",
                    metadata={"cpu": stats.get("cpu_usage"), "mem": stats.get("memory_usage")}
                )
                
                # 2. Swarm nodes and synaptic links
                peers = self.voyager_discovery.get_active_peers()
                for peer in peers:
                    peer_id = peer.get("properties", {}).get("node_id", peer["name"])
                    
                    # Estimate Link Strength based on mDNS response time if available
                    strength = 1.5 if peer.get("port") == 5555 else 0.8
                    
                    self.topology_reporter.record_node(peer_id, group="peer")
                    self.topology_reporter.record_link("localhost", peer_id, strength=strength)

                self.topology_reporter.export()
                await asyncio.sleep(10) # 10s Topology Pulse
            except Exception as e:
                logger.error(f"FleetManager: Topology Loop Error: {e}")
                await asyncio.sleep(5)


if __name__ == "__main__":
    # Test script for FleetManager
    logging.basicConfig(level=logging.INFO)
    root = Path(str(Path(__file__).resolve().parents[3]) + "")
    fleet = FleetManager(str(root))

    # These agents are used for the demo below
    from src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent
    from src.logic.agents.security.security_guard_agent import \
        SecurityGuardAgent

    fleet.register_agent(
        "Knowledge",
        KnowledgeAgent,
        str(root / "src/logic/agents/cognitive/knowledge_agent.py"),
    )
    fleet.register_agent(
        "Security",
        SecurityGuardAgent,
        str(root / "src.logic.agents.security.security_guard_agent.py"),
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
