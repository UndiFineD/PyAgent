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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Coordinator for deploying and aggregating results from multiple agents."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from pathlib import Path
from typing import Any, TYPE_CHECKING
from src.observability.StructuredLogger import StructuredLogger
from src.core.base.BaseAgent import BaseAgent
from src.core.base.models import AgentPriority
from src.infrastructure.fleet.WorkflowState import WorkflowState
from src.infrastructure.fleet.AgentRegistry import AgentRegistry
from src.infrastructure.fleet.OrchestratorRegistry import OrchestratorRegistry
from src.infrastructure.fleet.FleetExecutionCore import FleetExecutionCore
from src.infrastructure.fleet.FleetLifecycleManager import FleetLifecycleManager
from src.infrastructure.fleet.FleetInteractionRecorder import FleetInteractionRecorder
from src.infrastructure.fleet.FleetRoutingCore import FleetRoutingCore
from src.infrastructure.fleet.FleetConsensusManager import FleetConsensusManager

# Type Hinting Imports (Phase 106)
if TYPE_CHECKING:
    from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
    from src.infrastructure.backend.SqlMetadataHandler import SqlMetadataHandler
    from src.observability.stats.metrics_engine import ObservabilityEngine, ModelFallbackEngine
    from src.infrastructure.orchestration.ToolRegistry import ToolRegistry
    from src.infrastructure.orchestration.SignalRegistry import SignalRegistry
    from src.infrastructure.orchestration.SelfHealingOrchestrator import SelfHealingOrchestrator
    from src.infrastructure.orchestration.SelfImprovementOrchestrator import SelfImprovementOrchestrator
    from src.logic.agents.cognitive.context.engines.GlobalContextEngine import GlobalContextEngine

# Core Components

# Registry and Orchestrators
__version__ = VERSION

logger = StructuredLogger(__name__)




class FleetManager:
    """
    The central hub for the PyAgent ecosystem. Orchestrates a swarm of specialized
    agents to complete complex workflows, manages resource scaling, and ensures
    system-wide stability through various orchestrators.
    """

    def __getattr__(self, name: str) -> Any:
        """Delegate to orchestrators and agents for lazy loading support."""
        if name.startswith("__"):
            raise AttributeError(f"'FleetManager' object has no attribute '{name}'")

        # Optimization: Avoid recursion if we are already looking for an internal attribute
        current_dict = self.__dict__

        # Phase 130: Handle Backend -> System rename for legacy support
        effective_name = name
        if "backend" in name:
            effective_name = name.replace("backend", "system")

        # 1. Capability Hints Fallback (Phase 125: Check explicit mappings first)
        hints = getattr(self, "_capability_hints", {})
        if effective_name in hints:
            target = hints[effective_name]
            try:
                return getattr(self, target)
            except AttributeError:
                pass
        elif name != effective_name and name in hints:
            target = hints[name]
            try:
                return getattr(self, target)
            except AttributeError:
                pass

        # 2. Try Orchestrators
        if 'orchestrators' in current_dict:
            orchestrators = current_dict['orchestrators']
            try:
                # LazyOrchestratorMap implements __getattr__
                return getattr(orchestrators, effective_name)
            except AttributeError:
                if effective_name != name:
                    try:
                        return getattr(orchestrators, name)
                    except AttributeError:
                        pass
            except Exception as e:
                logging.debug(f"Fleet: Lazy-load error for orchestrator '{name}': {e}")

        # 3. Try Agents
        if 'agents' in current_dict:
            agents = current_dict['agents']
            try:
                # LazyAgentMap implements __getitem__ with fallback logic
                return agents[effective_name]
            except (KeyError, Exception):
                if effective_name != name:
                    try:
                        return agents[name]
                    except (KeyError, Exception):
                        pass

        raise AttributeError(f"'FleetManager' object has no attribute '{name}'")

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)

        # New: Lazy Orchestrators (replaces ~50 direct instantiations)
        self.orchestrators = OrchestratorRegistry.get_orchestrator_map(self)

        # Load agents from registry (also lazy)
        # Pass self so agents can register utils/tools upon lazy instantiation
        self.agents = AgentRegistry.get_agent_map(self.workspace_root, fleet_instance=self)

        # Capability Hints for Lazy Loading (Core Agents)
        self._capability_hints = {
            "articulate": "LinguisticAgent",
            "reason": "ReasoningAgent",
            "code": "CoderAgent",
            "sql": "SQLCoderAgent",
            "git": "PullRequestAgent",
            "teleport": "ModalTeleportationOrchestrator",  # Orchestrator logic
            "byzantine_judge": "ByzantineConsensusAgent",
            "governance": "GovernanceAgent",
            "immune_system": "ImmuneSystemAgent",
            "signal_bus": "SignalBusOrchestrator",
            "world_model": "WorldModelAgent",
            "nas": "NetworkArchSearchAgent",
            "heartbeat": "HeartbeatOrchestrator",
            "entanglement": "EntanglementOrchestrator",
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
            "feature_store": "FeatureStoreAgent",
            "inter_fleet_identity": "InterFleetIdentityAgent",
            "inter_fleet_bridge": "InterFleetBridgeOrchestrator",
            "synthetic_data": "SyntheticDataAgent",
            "graph_relational": "GraphRelationalAgent",
            "empathy_engine": "EmpathyAgent",
            "neurosymbolic": "NeuroSymbolicAgent",
            "neuro_symbolic": "NeuroSymbolicAgent",
            "agent_identity": "IdentityAgent"
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
        try:
            _ = self.orchestrators.discovery
        except Exception as e:
            logging.debug(f"Peer discovery initialization skipped or failed: {e}")

    @property
    def telemetry(self) -> ObservabilityEngine:
        return self.orchestrators.telemetry

    @property
    def registry(self) -> ToolRegistry:
        return self.orchestrators.registry

    @property
    def signals(self) -> SignalRegistry:
        return self.orchestrators.signals

    @property
    def recorder(self) -> LocalContextRecorder:
        return self.orchestrators.recorder

    @property
    def sql_metadata(self) -> SqlMetadataHandler:
        return self.orchestrators.sql_metadata

    @property
    def self_healing(self) -> SelfHealingOrchestrator:
        return self.orchestrators.self_healing

    @property
    def self_improvement(self) -> SelfImprovementOrchestrator:
        return self.orchestrators.self_improvement

    @property
    def global_context(self) -> GlobalContextEngine:
        return self.orchestrators.global_context

    @property
    def fallback(self) -> ModelFallbackEngine:
        return self.orchestrators.fallback_engine

    @property
    def core(self) -> Any:
        return self.orchestrators.core

    @property
    def rl_selector(self) -> Any:
        return getattr(self.orchestrators, "r_l_selector", None) or getattr(self.orchestrators, "rl_selector", None)

    # PHASE 260: Preemption Logic
    def preempt_lower_priority_tasks(self, new_priority: AgentPriority) -> None:
        """Suspends all tasks with lower priority than the new high-priority task."""
        for tid, data in self.active_tasks.items():
            if data['priority'].value > new_priority.value:
                logging.info(f"Preempting lower-priority task {tid} ({data['priority'].name})")
                for agent in data.get('agents', []):
                    if hasattr(agent, 'suspend'):
                        agent.suspend()

    def resume_tasks(self) -> None:
        """Resumes all suspended tasks if no critical tasks are running."""
        # Check if any Critical/High tasks are still active
        critical_active = any(d['priority'].value < AgentPriority.NORMAL.value for d in self.active_tasks.values())
        if not critical_active:
            for tid, data in self.active_tasks.items():
                for agent in data.get('agents', []):
                    if hasattr(agent, 'resume'):
                        agent.resume()

    async def execute_reliable_task(self, task: str, priority: AgentPriority = AgentPriority.NORMAL) -> str:
        """Executes a task using the 7-phase inner loop and linguistic articulation."""
        return await self.execution_core.execute_reliable_task(task, priority=priority)

    async def _record_success(self, res_or_prompt: Any, *args, **kwargs) -> None:
        """Records the success of a workflow step (Delegated)."""
        await self.interaction_recorder.record_success(res_or_prompt, *args, **kwargs)

    async def _record_failure(self, prompt: str, error: str, model: str) -> None:
        """Records errors, failures, and mistakes (Delegated)."""
        await self.interaction_recorder.record_failure(prompt, error, model)

    def register_remote_node(self, node_url: str, agent_names: list[str], remote_version: str = "1.0.0") -> str:
        """
        Registers a remote node and its available agents.
        Uses VersionGate to ensure compatibility (Phase 104).
        """
        from src.core.base.version import SDK_VERSION
        from src.infrastructure.fleet.VersionGate import VersionGate
        from src.infrastructure.fleet.RemoteAgentProxy import RemoteAgentProxy

        if not VersionGate.is_compatible(SDK_VERSION, remote_version):
            logging.warning(f"Fleet: Rejecting remote node {node_url} (Incompatible version {remote_version})")
            return

        self.remote_nodes.append(node_url)
        for name in agent_names:
            proxy = RemoteAgentProxy(
                str(self.workspace_root / f"remote_{name.lower()}.proxy"),
                node_url,
                name
            )
            self.agents[f"remote_{name}"] = proxy
            logging.info(f"Registered remote agent proxy: remote_{name} at {node_url}")

    async def call_by_capability(self, goal: str, **kwargs) -> str:
        """Finds an agent with the required capability and executes it with RL optimization."""
        return await self.routing_core.call_by_capability(goal, **kwargs)

    def register_agent(self, name: str, agent_class: type[BaseAgent], file_path: str | None = None) -> str:
        """Adds an agent to the fleet."""
        return self.lifecycle_manager.register_agent(name, agent_class, file_path)

    # --- Biological Cell-Swarm Pattern (Phase 17) ---

    def cell_divide(self, agent_name: str) -> str:
        """Simulates biological mitosis."""
        return self.lifecycle_manager.cell_divide(agent_name)

    def cell_differentiate(self, agent_name: str, specialization: str) -> str:
        """Changes an agent's characteristics."""
        return self.lifecycle_manager.cell_differentiate(agent_name, specialization)

    def cell_apoptosis(self, agent_name: str) -> str:










        """Cleanly shuts down and removes an agent."""
        return self.lifecycle_manager.cell_apoptosis(agent_name)

    async def execute_workflow(self, task: str, workflow_steps: list[dict[str, Any]], priority: AgentPriority = AgentPriority.NORMAL) -> str:




        """Runs a sequence of agent actions with shared state and signals."""
        return await self.execution_core.execute_workflow(task, workflow_steps, priority=priority)

    def execute_with_consensus(self, task: str, primary_agent: str | None = None, secondary_agents: list[str] | None = None) -> dict[str, Any]:
        """


        Executes a task across multiple agents and uses ByzantineConsensusAgent to pick the winner.
        """
        return self.consensus_manager.execute_with_consensus(task, primary_agent, secondary_agents)

    def route_task(self, task_type: str, task_data: Any) -> str:



        """
        Routes tasks based on system load and hardware availability (Phase 126).
        """
        return self.routing_core.route_task(task_type, task_data)





if __name__ == "__main__":
    # Test script for FleetManager
    logging.basicConfig(level=logging.INFO)
    root = Path(str(Path(__file__).resolve().parents[3]) + "")
    fleet = FleetManager(str(root))

    # These agents are used for the demo below
    from src.logic.agents.cognitive.KnowledgeAgent import KnowledgeAgent
    from src.logic.agents.development.SecurityGuardAgent import SecurityGuardAgent

    fleet.register_agent("Knowledge", KnowledgeAgent, str(root / "src/logic/agents/cognitive/KnowledgeAgent.py"))
    fleet.register_agent("Security", SecurityGuardAgent, str(root / "src/logic/agents/development/SecurityGuardAgent.py"))

    workflow = [
        {"agent": "Knowledge", "action": "scan_workspace", "args": ["KnowledgeAgent"]},
        {"agent": "Security", "action": "improve_content", "args": ["password = os.environ.get('DB_PASSWORD')"]}
    ]

    # report = fleet.execute_workflow("Initial Audit", workflow) # Async call, requires await or asyncio.run
    # For now, just logging calls replacement
    logger.info("FleetManager demo execution started")
    # print(report)
    # print("\nTelemetry Summary:")
    # print(json.dumps(fleet.telemetry.get_summary(), indent=2))
    if hasattr(fleet, 'telemetry'):
        logger.info("Telemetry Summary", summary=fleet.telemetry.get_summary())
