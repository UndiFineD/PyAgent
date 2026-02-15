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
Fleet Manager - Primary Swarm Coordinator

Coordinator for deploying and aggregating results from multiple agents.
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Typically initialized within the system lifecycle or via management scripts to orchestrate agent tasks.

WHAT IT DOES:
The FleetManager serves as the central nervous system of the PyAgent swarm. It handles:
1. Agent Registration & Lifecycle: Tracks active agents and their capabilities.
2. Task Distribution: Dispatches work chunks to specialized agents (e.g., CoderAgent, ResearchAgent).
3. Result Aggregation: Collects and synthesizes findings from across the fleet.
4. Resilience & Backup: Manages distributed state backups to prevent data loss.
5. Self-Improvement: Provides hooks for the EvolutionLoop to maintain system health.

WHAT IT SHOULD DO BETTER:
- Implement more advanced load balancing for agent task queues.
- Enhance real-time performance metrics tracking for individual agents.
- Support dynamic scaling of agent clusters based on workload complexity.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, cast

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
from src.infrastructure.swarm.orchestration.swarm.consensus import SwarmConsensus
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
from src.infrastructure.swarm.fleet.rl_selector import RLSelector
from src.observability.structured_logger import StructuredLogger
from src.infrastructure.swarm.topology_reporter import SwarmTopologyReporter
from src.infrastructure.security.firewall.zero_trust import ZeroTrustFirewall
from src.infrastructure.security.firewall.infection_guard import InfectionGuard
from src.infrastructure.swarm.orchestration.swarm.swarm_pruning_orchestrator import SwarmPruningOrchestrator

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

    def _safe_start_task(self, coro) -> None:
        """Starts a task if an event loop is running, otherwise logs a warning."""
        try:
            asyncio.create_task(coro)
        except RuntimeError:
            with contextlib.suppress(Exception):
                coro.close()
            task_name = getattr(getattr(coro, "cr_code", None), "co_name", "unknown")
            logging.debug(f"Fleet: Could not start task {task_name} - no event loop.")

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.manifest_repo = ManifestRepository()
        self.backup_node = DistributedBackup(node_id=f"node-{self.workspace_root.name}")
        self.evolution_loop: EvolutionLoop | None = None
        self.topology_reporter = SwarmTopologyReporter(
            output_path=str(self.workspace_root / "data" / "logs" / "topology.json")
        )

        # Phase 324: Zero-Trust Security (Pillar 7)
        self.firewall = ZeroTrustFirewall(owner_key=f"node-key-{self.workspace_root.name}")
        self.infection_guard = InfectionGuard(workspace_root=str(self.workspace_root))

        # Phase 319-320: Voyager P2P Transport & Discovery
        self.voyager_transport = VoyagerTransport()
        self.voyager_discovery = DiscoveryNode(node_name=f"Fleet-{self.workspace_root.name}")

        # Phase 3.0: Swarm Consensus (Decentralized State)
        self.swarm_consensus = SwarmConsensus(
            node_id=f"node-{self.workspace_root.name}",
            transport=self.voyager_transport
        )

        # Phase 326: Neural Pruning & Synaptic Decay (Pillar 6)
        self.pruning_orchestrator = SwarmPruningOrchestrator(self)

        # New: Lazy Orchestrators (replaces ~50 direct instantiations)
        self.orchestrators = OrchestratorRegistry.get_orchestrator_map(cast(FleetManager, self))

        # Load agents from registry (also lazy)
        # Pass self so agents can register utils/tools upon lazy instantiation
        self.agents = AgentRegistry.get_agent_map(self.workspace_root, fleet_instance=cast(FleetManager, self))

        # Phase 320: LAN Discovery
        self.init_discovery(agent_id=f"fleet-{self.workspace_root.name}")

        # Start voyager services (async)
        self._safe_start_task(self.voyager_transport.start_server(self._handle_voyager_message))
        self._safe_start_task(self.voyager_discovery.start_advertising())
        self._safe_start_task(self.voyager_discovery.start_discovery())

        # Swarm Singularity: Register peer discovery handler
        self.voyager_discovery.register_on_peer_added(self._on_voyager_peer_added)

        # Phase 320: Resource Monitoring & Autonomous Balancing
        self.resource_monitor = ResourceMonitor(fleet=self)
        self.borrowed_helpers: Dict[str, Any] = {}  # Phase 320: Cluster Balancing Helpers
        self._rl_selector = RLSelector()  # Phase 321: RL-based Routing
        self._safe_start_task(self.resource_monitor.start())
        self._safe_start_task(self._topology_loop())

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
        self.execution_core = FleetExecutionCore(cast(FleetManager, self))
        self.lifecycle_manager = FleetLifecycleManager(cast(FleetManager, self))
        self.interaction_recorder = FleetInteractionRecorder(cast(FleetManager, self))
        self.routing_core = FleetRoutingCore(cast(FleetManager, self))
        self.consensus_manager = FleetConsensusManager(cast(FleetManager, self))

        # Phase 123: Start Peer Discovery
        with contextlib.suppress(Exception):
            _ = self.orchestrators.discovery

        # Defer EvolutionLoop initialization until FleetManager is fully constructed
        self.evolution_loop = EvolutionLoop(cast(FleetManager, self))

        # Start evolution loop now that it's initialized
        self._safe_start_task(self.evolution_loop.start())

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
            # Check for UniversalAgent in capability hints
            if "universal" in self.capability_hints:
                target_agent = self.capability_hints["universal"]
                logger.info(f"FleetManager: Dispatched to {target_agent} (Pillar 3)")

                result = await cast(FleetDelegationMixin, self).delegate_to(target_agent, command)

                # Record response
                self.interaction_recorder.record_interaction(
                    user_input=command,
                    agent_id=target_agent,
                    role="assistant",
                    content=str(result)
                )
                return {"status": "success", "agent": target_agent, "result": result}

            # Fallback to standard delegation
            target_agent = "ReasoningAgent"
            if "code" in command.lower() or "fix" in command.lower():
                target_agent = "CoderAgent"

            result = await cast(FleetDelegationMixin, self).delegate_to(target_agent, command)
            return {"status": "success", "agent": target_agent, "result": result}

        except (ValueError, TypeError, RuntimeError, asyncio.TimeoutError) as e:
            logger.error(f"FleetManager: Agent delegation failed: {e}")
            # Final fallback to ReasoningAgent
            try:
                result = await cast(FleetDelegationMixin, self).delegate_to("ReasoningAgent", command)
                return {"status": "success", "agent": "ReasoningAgent", "result": result}
            except (ValueError, TypeError, RuntimeError, asyncio.TimeoutError) as e2:
                return {"status": "error", "message": str(e2)}

    # Logic delegated to mixins

    async def _on_voyager_peer_added(self, peer_data: Dict[str, Any]) -> None:
        """P2P Handshake & Consensus setup for newly discovered Voyager peers."""
        peer_id = peer_data["properties"].get("node_id", peer_data["name"])
        addrs = peer_data["addresses"]
        if not addrs:
            return
        addr = addrs[0]
        port = int(peer_data["properties"].get("transport_port", 5555))

        # 1. E2EE Handshake (Double Ratchet Phase 2.0)
        if peer_id not in self.voyager_transport.sessions:
            logger.info(f"Voyager: Initiating Double Ratchet session with {peer_id}...")
            response = await self.voyager_transport.send_to_peer(
                addr, port,
                {
                    "type": "HANDSHAKE_INIT",
                    "sender_id": f"node-{self.workspace_root.name}",
                    "public_key": b"node-v4-init-pub"
                },
                peer_id=peer_id
            )

            if response and response.get("type") == "HANDSHAKE_RESPONSE":
                from src.infrastructure.security.encryption.double_ratchet import \
                    DoubleRatchet
                remote_pub = response.get("public_key")
                # Phase 2.0: Shared secret established (simulated DH)
                root_key = b"swarm-shared-secret-v4"
                if remote_pub is None:
                    remote_pub = b"peer-ephemeral-pub-default"
                self.voyager_transport.sessions[peer_id] = DoubleRatchet(root_key, remote_pub)
                logger.info(f"Voyager: E2EE Session active with {peer_id}")

        # 2. Update Consensus Registry
        current_peers = [p["properties"].get("node_id", p["name"])
                         for p in self.voyager_discovery.get_active_peers()]
        self.swarm_consensus.set_peers(current_peers)

    async def _handle_voyager_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handles incoming P2P messages from the Voyager transport layer."""
        # Phase 324: Zero-Trust Validation (Pillar 7)
        signature = message.get("signature", "unsigned")
        sender_id = message.get("sender_id", "unknown")

        if not self.firewall.validate_message(message, signature, sender_id):
            logger.warning(f"FleetManager: Blocked message from {sender_id} - Zero-Trust Violation")
            return {"status": "error", "reason": "security_violation"}

        # Phase 324: Infection Guard (Instruction Validation)
        if not self.infection_guard.validate_instruction(sender_id, message):
            logger.warning(f"FleetManager: Blocked malicious instruction from {sender_id}")
            return {"status": "error", "reason": "infection_guard_blocked"}

        msg_type = message.get("type")

        if msg_type == "delegate_task":
            agent_type = message.get("agent_type")
            prompt = message.get("prompt")
            if not isinstance(agent_type, str):
                return {"status": "error", "message": "agent_type must be a string"}
            if not isinstance(prompt, str):
                return {"status": "error", "message": "prompt must be a string"}
            try:
                result = await self.delegate_to(agent_type, prompt)
                return {"status": "success", "result": result}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        elif msg_type and msg_type.startswith("CONSENSUS_"):
            # Update peer list for consensus engine
            peers = [p["name"] for p in self.voyager_discovery.get_active_peers()]
            self.swarm_consensus.set_peers(peers)
            return self.swarm_consensus.handle_message(message)

        elif msg_type == "HANDSHAKE_INIT":
            # Start Double Ratchet Session (Phase 2.0 Security)
            remote_pub = message.get("public_key")
            # In a real implementation, we'd do X3DH or similar
            # For Phase 3.0, we simulate with a dummy root key
            from src.infrastructure.security.encryption.double_ratchet import DoubleRatchet
            root_key = b"swarm-shared-secret-v4"
            if remote_pub is None:
                remote_pub = b"peer-ephemeral-pub-default"
            self.voyager_transport.sessions[sender_id] = DoubleRatchet(root_key, remote_pub)
            return {"type": "HANDSHAKE_RESPONSE", "public_key": b"local-ephemeral-pub"}

        elif msg_type == "compute_borrow_request":
            # Python MPI: Evaluate if we have idle capacity (<50%) to help a neighbor
            stats = self.resource_monitor.get_latest_stats()
            cpu = stats.get("cpu_usage", 0.0)
            mem = stats.get("memory_usage", 0.0)

            if cpu < 50.0 and mem < 60.0:
                logger.info(f"FleetManager: Accepting compute-borrow from {sender_id}. Current Load: {cpu}%")
                return {"status": "can_help", "node_id": f"node-{self.workspace_root.name}"}
            else:
                return {"status": "too_busy"}

        elif msg_type == "resource_status":
            return {"status": "ok"}

        elif msg_type == "shard_store" or msg_type == "store_shard":
            shard = message.get("shard", {})
            success = self.backup_node.store_shard_locally(shard)
            return {"status": "success" if success else "error"}

        elif msg_type == "shard_request" or msg_type == "request_shard":
            state_hash = message.get("hash")
            if not isinstance(state_hash, str):
                return {"status": "error", "message": "hash must be a string"}
            shards = self.backup_node.get_local_shards_for_hash(state_hash)
            return {"status": "success", "shards": shards}

        elif msg_type == "hologram_projection":
            # Phase 330: Holographic Metadata Projection
            if hasattr(self.orchestrators, "holographic_state"):
                await self.orchestrators.holographic_state.handle_projection(message)
            return {"status": "ok"}

        elif msg_type == "hologram_shard_request":
            # Phase 330: Perspective-specific shard retrieval
            h_id = message.get("hologram_id")
            if hasattr(self.orchestrators, "holographic_state"):
                shards = await self.orchestrators.holographic_state.find_local_hologram_shards(h_id)
                return {"status": "success", "shards": shards}
            return {"status": "error", "reason": "no_holographic_orchestrator"}

        return {"status": "unknown_message_type"}

    async def _topology_loop(self) -> None:
        """Periodically refreshes the swarm topology visualization data (Pillar 9)."""
        while True:
            try:
                # 1. Fresh start for the current pulse (Pillar 6 Synaptic Modularization)
                self.topology_reporter.clear_snapshot()

                # 2. Self node with Resource metrics
                stats = self.resource_monitor.get_latest_stats()
                traffic = stats.get("network_io", {}).get("bytes_sent", 0)
                self.topology_reporter.update_traffic("localhost", traffic)

                self.topology_reporter.record_node(
                    node_id="localhost",
                    group="gateway",
                    metadata={"cpu": stats.get("cpu_usage"), "mem": stats.get("memory_usage")}
                )

                # 3. Active Local Agents (Synaptic Connections)
                for agent_id in self.agents.keys():
                    self.topology_reporter.record_node(agent_id, group="agent")
                    self.topology_reporter.record_link("localhost", agent_id, strength=1.2, type="memory_bus")

                # 4. Swarm nodes and synaptic links
                peers = self.voyager_discovery.get_active_peers()
                for peer in peers:
                    peer_id = peer.get("properties", {}).get("node_id", peer["name"])

                    # Estimate Link Strength based on connection status
                    strength = 1.5 if peer.get("port") == 5555 else 0.8

                    self.topology_reporter.record_node(peer_id, group="peer")
                    self.topology_reporter.record_link("localhost", peer_id, strength=strength, type="voyager_p2p")

                self.topology_reporter.export()
                await asyncio.sleep(300)  # 5m Topology Pulse
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
