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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Coordinator for deploying and aggregating results from multiple agents."""



import logging
import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Type, TYPE_CHECKING
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# Type Hinting Imports (Phase 106)
if TYPE_CHECKING:
    from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
    from src.infrastructure.backend.SqlMetadataHandler import SqlMetadataHandler

# Core Components
from src.core.base.BaseAgent import BaseAgent
from src.infrastructure.fleet.WorkflowState import WorkflowState

# Registry and Orchestrators
from src.infrastructure.fleet.AgentRegistry import AgentRegistry
from src.infrastructure.fleet.OrchestratorRegistry import OrchestratorRegistry
from src.infrastructure.fleet.FleetExecutionCore import FleetExecutionCore
from src.infrastructure.fleet.FleetLifecycleManager import FleetLifecycleManager

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
            "teleport": "ModalTeleportationOrchestrator", # Orchestrator logic
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
            "honeypot": "HoneypotAgent",
            "consensus_orchestrator": "ConsensusOrchestrator",
            "speciation_orchestrator": "SpeciationOrchestrator",
            "feature_store": "FeatureStoreAgent",
            "inter_fleet_identity": "InterFleetIdentityAgent",
            "inter_fleet_bridge": "InterFleetBridgeOrchestrator"
        }
        
        self.remote_nodes: List[str] = []
        self.state: Optional[WorkflowState] = None
        self.action_history: List[str] = [] # For loop detection
        self.kill_switch = False # Emergency termination

        # Delegated Managers (Phase 120 Extraction)
        self.execution_core = FleetExecutionCore(self)
        self.lifecycle_manager = FleetLifecycleManager(self)
        
        # Phase 123: Start Peer Discovery
        try:
            _ = self.orchestrators.discovery
        except Exception as e:
            logging.debug(f"Peer discovery initialization skipped or failed: {e}")

    @property
    def telemetry(self) -> "ObservabilityEngine":
        return self.orchestrators.telemetry

    @property
    def registry(self) -> "ToolRegistry":
        return self.orchestrators.registry

    @property
    def signals(self) -> "SignalRegistry":
        return self.orchestrators.signals

    @property
    def recorder(self) -> "LocalContextRecorder":
        return self.orchestrators.recorder

    @property
    def sql_metadata(self) -> "SqlMetadataHandler":
        return self.orchestrators.sql_metadata

    @property
    def self_healing(self) -> "SelfHealingOrchestrator":
        return self.orchestrators.self_healing

    @property
    def self_improvement(self) -> "SelfImprovementOrchestrator":
        return self.orchestrators.self_improvement

    @property
    def global_context(self) -> "GlobalContextEngine":
        return self.orchestrators.global_context

    @property
    def fallback(self) -> "ModelFallbackEngine":
        return self.orchestrators.fallback_engine

    @property
    def core(self) -> Any:
        return self.orchestrators.core

    @property
    def rl_selector(self) -> Any:
        return getattr(self.orchestrators, "r_l_selector", None) or getattr(self.orchestrators, "rl_selector", None)

    async def execute_reliable_task(self, task: str) -> str:
        """Executes a task using the 7-phase inner loop and linguistic articulation."""
        return await self.execution_core.execute_reliable_task(task)

    async def _record_success(self, res_or_prompt: Any, *args, **kwargs) -> None:
        """Records the success of a workflow step including Explainability and Telemetry."""
        # Detect calling convention (New: 8 parameters total, Legacy: 3)
        # In *args, New convention has exactly 7 items.
        if len(args) == 7:
             # New convention: res, workflow_id, agent_name, action_name, args, token_info, trace_id, start_time
             res = res_or_prompt
             workflow_id, agent_name, action_name, p_args, token_info, trace_id, start_time = args
             duration = time.time() - start_time
             prompt = f"{agent_name}.{action_name}({p_args})"
             model = token_info.get("model", "unknown")
        else:
             # Legacy convention: prompt, result, model
             prompt = res_or_prompt
             res = args[0] if args else "n/a"
             model = args[1] if len(args) > 1 else "unknown"
             workflow_id = "legacy"
             agent_name = "FleetManager"
             action_name = "execute"
             duration = 0
             trace_id = "none"
             token_info = {"model": model}

        # 1. Standard Interaction Logging
        try:
            self.recorder.record_interaction(
                provider="fleet_internal",
                model=model,
                prompt=prompt,
                result=str(res),
                meta={"workflow_id": workflow_id, "duration": duration, "trace_id": trace_id}
            )
        except Exception:
            pass

        # 2. Phase 125: Explainability Trace
        try:
            explainability = getattr(self, "explainability", None)
            if explainability:
                justification = explainability.justify_action(agent_name, action_name, res)
                explainability.log_reasoning_step(
                    workflow_id=workflow_id,
                    agent_name=agent_name,
                    action=action_name,
                    justification=justification,
                    context={"input_args": locals().get("p_args", []), "token_usage": token_info}
                )
        except Exception:
            pass

        # 3. Telemetry
        try:
            self.telemetry.record_event("action_success", {
                "agent": agent_name,
                "action": action_name,
                "workflow": workflow_id
            })
        except Exception:
            pass

    async def _record_failure(self, prompt: str, error: str, model: str) -> None:
        """Records errors, failures, and mistakes for collective intelligence (Phase 108)."""
        try:
            # Phase 152: Use aiofiles for non-blocking IO
            import aiofiles
            
            # Use the sharded recorder for centralized intelligence harvesting
            # We assume recorder supports async or we offload it
            self.recorder.record_interaction(
                provider="fleet_internal",
                model=model,
                prompt=prompt,
                result=f"ERROR: {error}",
                meta={"status": "failed"}
            )
            
            # Persistent audit log
            failure_log = self.workspace_root / "data/logs" / "fleet_failures.jsonl"
            failure_log.parent.mkdir(parents=True, exist_ok=True)
            from datetime import datetime
            record = {
                "timestamp": datetime.now().isoformat(),
                "model": model,
                "prompt": prompt[:500],
                "error": error
            }
            async with aiofiles.open(failure_log, "a", encoding="utf-8") as f:
                await f.write(json.dumps(record) + "\n")
        except Exception:
            logging.error("Failed to write to fleet_failures.jsonl log.")

    def register_remote_node(self, node_url: str, agent_names: List[str], remote_version: str = "1.0.0") -> str:
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
        # Report activity to TemporalSync
        if hasattr(self, 'temporal_sync'):
            self.temporal_sync.report_activity()
            
        g_low = goal.lower()
        
        # New: Capability Hint Lookup
        for hint_key, agent_name in self._capability_hints.items():
            if hint_key in g_low and agent_name in self.agents:
                _ = self.agents[agent_name] # Force load
                logging.info(f"Fleet: Lazy-loaded '{agent_name}' for capability '{hint_key}'")

        # New: Auto-instantiate agent if goal matches agent name
        if goal in self.agents:
            _ = self.agents[goal] # Access triggers instantiation and tool registration
        else:
            # Check if any agent name contains the goal
            for agent_name in self.agents:
                if g_low in agent_name.lower():
                    _ = self.agents[agent_name]
                    break
            
        # Get tool metadata for scoring
        tools = self.registry.list_tools()
        tools_metadata = []
        for t in tools:
            tools_metadata.append({
                "name": t.name,
                "owner": t.owner,
                "sync": getattr(t, 'sync', True) # Optimization: check if tool can be run async
            })
            
        scored_candidates = self.core.score_tool_candidates(goal, tools_metadata, kwargs)
        
        if not scored_candidates:
            return f"No tool found for goal: {goal}"
            
        candidates = [c[1] for c in scored_candidates]
        
        # Phase 123: Robust RL Selection with Fallback
        selector = self.rl_selector
        if selector and hasattr(selector, "select_best_tool"):
            best_tool = selector.select_best_tool(candidates)
            logging.info(f"Fleet selected optimized tool '{best_tool}' using RL for goal '{goal}'")
        else:
            best_tool = candidates[0]
            logging.info(f"Fleet: RLSelector missing or incompatible. Defaulting to first candidate '{best_tool}' for goal '{goal}'")
        
        # Determine if tool is essential (Bootstrap)
        owner = next((t.owner for t in tools if t.name == best_tool), None)
        is_essential = owner in self.agents.registry_configs if owner else False
        
        start_time = time.time()
        try:
            import asyncio
            async def run_tool() -> str:
                if asyncio.iscoroutinefunction(self.registry.call_tool):
                    return await self.registry.call_tool(best_tool, **kwargs)
                else:
                    loop = asyncio.get_running_loop()
                    return await loop.run_in_executor(None, self.registry.call_tool, best_tool, **kwargs)

            if is_essential:
                res = await run_tool()
            else:
                try:
                    res = await asyncio.wait_for(run_tool(), timeout=5.0)
                except asyncio.TimeoutError:
                    error_msg = f"Non-essential tool '{best_tool}' (owner: {owner}) timed out after 5 seconds."
                    logging.warning(error_msg)
                    return error_msg

            # Phase 123: Security Audit Feedback Loop
            audit_passed = True
            if "ImmuneSystem" in self.agents:
                try:
                    immune = self.agents["ImmuneSystem"]
                    if asyncio.iscoroutinefunction(immune.perform_security_audit):
                        audit_passed = await immune.perform_security_audit(best_tool, str(res))
                    else:
                        audit_passed = immune.perform_security_audit(best_tool, str(res))
                except Exception:
                    pass
            
            if not audit_passed:
                logging.warning(f"Fleet: Security audit FAILED for tool '{best_tool}'. Penalizing RLSelector.")
                if self.rl_selector: self.rl_selector.update_stats(best_tool, success=False)
                return f"ERROR: Security audit failed for tool '{best_tool}'. Output blocked."

            if self.rl_selector: self.rl_selector.update_stats(best_tool, success=True)
            # Record for future improvements
            await self._record_success(f"Capability call: {goal} with {kwargs}", str(res), "internal_ai")
            return res
        except Exception as e:
            if self.rl_selector: self.rl_selector.update_stats(best_tool, success=False)
            logging.error(f"Error executing tool {best_tool}: {e}")
            # Self-healing attempt
            if self.self_healing:
                target_agent = owner if owner else best_tool
                clean_kwargs = {k: v for k, v in kwargs.items() if k != "agent_name"}
                if asyncio.iscoroutinefunction(self.self_healing.attempt_repair):
                    return await self.self_healing.attempt_repair(target_agent, e, **clean_kwargs)
                else:
                    return self.self_healing.attempt_repair(target_agent, e, **clean_kwargs)
            return f"Error executing tool {best_tool}: {e}"
        finally:
            if hasattr(self, 'telemetry'):
                self.telemetry.trace_workflow(f"tool_{best_tool}", time.time() - start_time)
        
    def register_agent(self, name: str, agent_class: Type[BaseAgent], file_path: Optional[str] = None) -> str:
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

    async def execute_workflow(self, task: str, workflow_steps: List[Dict[str, Any]]) -> str:
        """Runs a sequence of agent actions with shared state and signals."""
        return await self.execution_core.execute_workflow(task, workflow_steps)

    def execute_with_consensus(self, task: str, primary_agent: str = None, secondary_agents: List[str] = None) -> Dict[str, Any]:
        """
        Executes a task across multiple agents and uses ByzantineConsensusAgent to pick the winner.
        If agents are not specified, ByzantineConsensusAgent dynamically selects a committee. (Phase 123)
        """
        logging.info(f"Fleet: Running consensus vote for task: {task[:50]}")
        
        # Phase 123: Dynamic Committee Formation
        if not primary_agent or not secondary_agents:
            # Look in both registry configs (bootstrap) and currently loaded/discovered agents
            available = list(set(list(self.agents.registry_configs.keys()) + list(self.agents.keys())))
            # Exclude judge and self
            available = [a for a in available if a not in ["ByzantineConsensus", "ByzantineConsensusAgent", "FleetManager"]]
            
            # Use case-insensitive lazy access (ByzantineConsensus)
            judge = getattr(self, "ByzantineConsensus", None)
            if not judge:
                # Attempt to find it by variant names
                for name in ["byzantine_judge", "ByzantineConsensusAgent"]:
                    judge = getattr(self, name, None)
                    if judge: break
            
            if not judge:
                return {"decision": "REJECTED", "reason": "ByzantineConsensus agent not available."}
                
            committee = judge.select_committee(task, available)
            if not committee:
                return {"decision": "REJECTED", "reason": "No committee could be formed."}
            primary_agent = committee[0]
            secondary_agents = committee[1:]
            logging.info(f"Fleet: Formed dynamic committee: {primary_agent}, {secondary_agents}")

        proposals: Dict[str, str] = {}
        all_agents = [primary_agent] + secondary_agents
        
        for agent_name in all_agents:
            if agent_name in self.agents:
                try:
                    # Defaulting to 'improve_content' for the consensus pool
                    res = self.agents[agent_name].improve_content(task)
                    proposals[agent_name] = res
                except Exception as e:
                    logging.error(f"Fleet: Agent {agent_name} failed to provide consensus proposal: {e}")

        if not proposals:
            return {"decision": "REJECTED", "reason": "No agents could provide proposals."}

        # Run the committee vote
        # Use the judge found earlier or the lazy access
        if 'judge' not in locals():
            judge = getattr(self, "ByzantineConsensus", None)
            
        if not judge:
            return {"decision": "REJECTED", "reason": "ByzantineConsensus not found for voting."}

        result = judge.run_committee_vote(task, proposals)
        
        # If success, broadcast lesson via Federated Knowledge
        if result["decision"] == "ACCEPTED" and getattr(self, "federated_knowledge", None):
            try:
                self.federated_knowledge.broadcast_lesson(
                    lesson_id=f"consensus_{int(time.time())}",
                    lesson_data={
                        "agent": result.get("winner"),
                        "task_type": "high_integrity_code",
                        "success": True,
                        "fix": f"Consensus reached by {result.get('winner')} for {task[:30]}"
                    }
                )
            except Exception:
                pass
            
        return result

    def route_task(self, task_type: str, task_data: Any) -> str:
        """
        Routes tasks based on system load and hardware availability (Phase 126).
        """
        stats = self.telemetry.orchestrator.monitor.get_current_stats()
        
        # Logic for compute-heavy tasks (e.g., training, large-scale indexing)
        is_compute_heavy = task_type in ["training", "indexing", "llm_finetune"]
        
        if is_compute_heavy and stats["gpu"]["available"]:
            logging.info(f"Fleet: Routing {task_type} to GPU node ({stats['gpu']['type']})")
            return f"ROUTED:GPU:{stats['gpu']['type']}"
        elif is_compute_heavy and stats["status"] == "CRITICAL":
            logging.warning("Fleet: System critical, deferring compute-heavy task.")
            return "DEFERRED:LOAD_CRITICAL"
        
        logging.info(f"Fleet: Routing {task_type} to standard CPU pool.")
        return "ROUTED:CPU:POOL"


if __name__ == "__main__":
    # Test script for FleetManager
    logging.basicConfig(level=logging.INFO)
    root = Path("c:/DEV/PyAgent")
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
    
    report = fleet.execute_workflow("Initial Audit", workflow)
    print(report)
    print("\nTelemetry Summary:")
    print(json.dumps(fleet.telemetry.get_summary(), indent=2))
