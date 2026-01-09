#!/usr/bin/env python3

"""Coordinator for deploying and aggregating results from multiple agents."""

import logging
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Type, TYPE_CHECKING
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# Type Hinting Imports (Phase 106)
if TYPE_CHECKING:
    from src.classes.backend.LocalContextRecorder import LocalContextRecorder
    from src.classes.backend.SqlAgent import SqlAgent
    from src.classes.stats.ObservabilityEngine import ObservabilityEngine
    from src.classes.orchestration.ToolRegistry import ToolRegistry
    from src.classes.orchestration.SignalRegistry import SignalRegistry
    from src.classes.stats.ModelFallbackEngine import ModelFallbackEngine
    from src.classes.context.GlobalContextEngine import GlobalContextEngine
    from src.classes.orchestration.SelfHealingOrchestrator import SelfHealingOrchestrator
    from src.classes.orchestration.SelfImprovementOrchestrator import SelfImprovementOrchestrator

# Core Components
from src.classes.base_agent import BaseAgent
from src.classes.fleet.WorkflowState import WorkflowState

# Registry and Orchestrators
from src.classes.fleet.AgentRegistry import AgentRegistry
from src.classes.fleet.OrchestratorRegistry import OrchestratorRegistry

class FleetManager:
    """
    The central hub for the PyAgent ecosystem. Orchestrates a swarm of specialized
    agents to complete complex workflows, manages resource scaling, and ensures
    system-wide stability through various orchestrators.
    """
    
    def __getattr__(self, name: str) -> Any:
        """Delegate to orchestrators and agents for lazy loading support."""
        if 'orchestrators' in self.__dict__:
            try:
                # Direct check to avoid recursion if orchestrators is missing
                return getattr(self.orchestrators, name)
            except (AttributeError, KeyError):
                pass

        if 'agents' in self.__dict__:
            try:
                # LazyAgentMap handles case-insensitive lookup
                return self.agents[name]
            except (KeyError, AttributeError):
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
            "sql": "SQLAgent",
            "git": "PRAgent",
            "teleport": "ModalTeleportationOrchestrator" # Orchestrator logic
        }
        
        self.remote_nodes: List[str] = []
        self.state: Optional[WorkflowState] = None
        self.action_history: List[str] = [] # For loop detection
        self.kill_switch = False # Emergency termination

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
    def sql_metadata(self) -> "SqlAgent":
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

    def execute_reliable_task(self, task: str) -> str:
        """Executes a task using the 7-phase inner loop and linguistic articulation."""
        # Preference: Use Internal AI if available, else route
        current_model = "internal_ai"
        try:
            if hasattr(self, 'router_model'):
                current_model = self.router_model.determine_optimal_provider(task)
            logging.info(f"Fleet selected model '{current_model}' for task.")
        except Exception:
            logging.debug("Defaulting to internal_ai model.")

        try:
            technical_report = self.structured_orchestrator.execute_task(task)
            res = self.linguist.articulate_results(technical_report, task)
            
            # Record success (for training the trillion parameter model)
            self._record_success(task, res, current_model)
            return res
        except Exception as e:
            # Record error/failure specifically for self-healing improvement
            self._record_failure(task, str(e), current_model)
            
            logging.error(f"Fleet failure: {e}")
            # Self-healing: Attempt fallback
            fallback_model = self.fallback_engine.get_fallback_model(current_model, str(e))
            if fallback_model and fallback_model != current_model:
                logging.warning(f"Self-Healing: Retrying with fallback model {fallback_model}...")
                try:
                    technical_report = self.structured_orchestrator.execute_task(task)
                    return self.linguist.articulate_results(technical_report, task)
                except Exception as e2:
                    logging.critical(f"Self-Healing: Fallback also failed: {e2}")
            raise

    def _record_success(self, prompt: str, result: str, model: str) -> str:
        """Records the unique context, prompt and result for future reference."""
        try:
            # Use the lazy-loaded recorder for speed and efficiency
            self.recorder.record_interaction(
                provider="fleet_internal",
                model=model,
                prompt=prompt,
                result=result
            )
        except Exception as e:
            # Silent failure for non-critical logging
            pass

    def _record_failure(self, prompt: str, error: str, model: str) -> None:
        """Records errors, failures, and mistakes for collective intelligence (Phase 108)."""
        try:
            # Use the sharded recorder for centralized intelligence harvesting
            self.recorder.record_interaction(
                provider="fleet_internal",
                model=model,
                prompt=prompt,
                result=f"ERROR: {error}",
                meta={"status": "failed"}
            )
            
            # Persistent audit log
            failure_log = self.workspace_root / "logs" / "fleet_failures.jsonl"
            failure_log.parent.mkdir(parents=True, exist_ok=True)
            from datetime import datetime
            record = {
                "timestamp": datetime.now().isoformat(),
                "model": model,
                "prompt": prompt[:500],
                "error": error
            }
            with open(failure_log, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except Exception:
            pass

    def register_remote_node(self, node_url: str, agent_names: List[str], remote_version: str = "1.0.0") -> str:
        """
        Registers a remote node and its available agents.
        Uses VersionGate to ensure compatibility (Phase 104).
        """
        from src.version import SDK_VERSION
        from src.classes.fleet.VersionGate import VersionGate
        
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

    def call_by_capability(self, goal: str, **kwargs) -> str:
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
        
        best_tool = self.rl_selector.select_best_tool(candidates)
        logging.info(f"Fleet selected optimized tool '{best_tool}' using RL for goal '{goal}'")
        
        # Determine if tool is essential (Bootstrap)
        # Tool owner is typical the agent name.
        owner = next((t.owner for t in tools if t.name == best_tool), None)
        is_essential = owner in self.agents.registry_configs if owner else False
        
        start_time = time.time()
        try:
            if is_essential:
                res = self.registry.call_tool(best_tool, **kwargs)
            else:
                # Non-essential components have a 5-second timeout (Phase 104)
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(self.registry.call_tool, best_tool, **kwargs)
                    try:
                        res = future.result(timeout=5.0)
                    except TimeoutError:
                        error_msg = f"Non-essential tool '{best_tool}' (owner: {owner}) timed out after 5 seconds."
                        logging.warning(error_msg)
                        return error_msg

            self.rl_selector.update_stats(best_tool, success=True)
            # Record for future improvements
            self._record_success(f"Capability call: {goal} with {kwargs}", str(res), "internal_ai")
            return res
        except Exception as e:
            self.rl_selector.update_stats(best_tool, success=False)
            logging.error(f"Error executing tool {best_tool}: {e}")
            # Self-healing attempt
            if self.self_healing:
                return self.self_healing.attempt_repair(best_tool, e, **kwargs)
            return f"Error executing tool {best_tool}: {e}"
        finally:
            if hasattr(self, 'telemetry'):
                self.telemetry.trace_workflow(f"tool_{best_tool}", time.time() - start_time)
        
    def register_agent(self, name: str, agent_class: Type[BaseAgent], file_path: Optional[str] = None) -> str:
        """Adds an agent to the fleet."""
        path = file_path or str(self.workspace_root / f"agent_{name.lower()}.py")
        self.agents[name] = agent_class(path)
        logging.info(f"Registered agent: {name}")

    # --- Biological Cell-Swarm Pattern (Phase 17) ---
    
    def cell_divide(self, agent_name: str) -> str:
        """
        Simulates biological mitosis by creating a clone of an existing agent.
        """
        if agent_name not in self.agents:
            return f"Error: Agent {agent_name} not found for division."
        
        base_agent = self.agents[agent_name]
        clone_name = f"{agent_name}_clone_{int(logging.time.time())}"
        
        # In a real system, we'd instantiate a new object of the same class
        # For this logic, we'll register it in the fleet as a new entry
        self.agents[clone_name] = base_agent # Simplified: sharing the instance for demo
        
        logging.info(f"Mitosis: {agent_name} divided into {clone_name}")
        self.signals.emit("CELL_DIVIDED", {"parent": agent_name, "child": clone_name}, sender="FleetManager")
        return f"Agent {agent_name} successfully divided into {clone_name}."

    def cell_differentiate(self, agent_name: str, specialization: str) -> str:
        """
        Changes an agent's characteristics or 'role' based on environmental signals.
        """
        if agent_name not in self.agents:
            return f"Error: Agent {agent_name} not found for differentiation."
            
        agent = self.agents[agent_name]
        # Simulate differentiation by updating system prompt or model
        logging.info(f"Differentiation: {agent_name} specialized into {specialization}")
        self.signals.emit("CELL_DIFFERENTIATED", {"agent": agent_name, "specialization": specialization}, sender="FleetManager")
        return f"Agent {agent_name} successfully differentiated into {specialization}."

    def cell_apoptosis(self, agent_name: str) -> str:
        """
        Cleanly shuts down and removes an agent from the fleet (programmed cell death).
        """
        if agent_name not in self.agents:
            return f"Error: Agent {agent_name} not found for apoptosis."
            
        del self.agents[agent_name]
        logging.info(f"Apoptosis: {agent_name} has been recycled.")
        self.signals.emit("CELL_APOPTOSIS", {"agent": agent_name}, sender="FleetManager")
        return f"Agent {agent_name} successfully removed from the fleet."

    def execute_workflow(self, task: str, workflow_steps: List[Dict[str, Any]]) -> str:
        """Runs a sequence of agent actions with shared state and signals."""
        if self.kill_switch:
            logging.error("Fleet KILL SWITCH active. Workflow terminated immediately.")
            return "ERROR: Fleet Terminal Kill Switch Active."

        # Ethics Review
        ethics_report = self.ethics_guardrail.review_task(task)
        if ethics_report["status"] == "rejected":
            logging.error(f"Ethics Review REJECTED: {ethics_report['violations']}")
            self.signals.emit("WORKFLOW_REJECTED", {"task": task, "violations": ethics_report["violations"]}, sender="FleetManager")
            return f"ERROR: Task rejected by Ethics Guardrail: {ethics_report['violations']}"

        results = []
        workflow_id = f"workflow_{int(logging.time.time())}"
        
        self.signals.emit("WORKFLOW_STARTED", {"task": task, "workflow_id": workflow_id}, sender="FleetManager")
        
        # Initialize Workflow State
        self.state = WorkflowState(task_id=workflow_id, original_request=task)
        self.state.set("task", task)
        
        for step in workflow_steps:
            if self.kill_switch:
                logging.error("Fleet KILL SWITCH triggered during workflow.")
                break

            agent_name = step.get("agent")
            action_name = step.get("action")
            args = step.get("args", [])
            
            # Dynamic argument injection from state
            processed_args = []
            for arg in args:
                if isinstance(arg, str) and arg.startswith("$"):
                    var_name = arg[1:]
                    processed_args.append(self.state.get(var_name, arg))
                else:
                    processed_args.append(arg)
            
            if agent_name not in self.agents:
                err = f"Error: Agent '{agent_name}' not found."
                results.append(err)
                self.signals.emit("AGENT_NOT_FOUND", {"agent": agent_name, "step": step}, sender="FleetManager")
                continue
                
            agent = self.agents[agent_name]
            if not hasattr(agent, action_name):
                err = f"Error: Action '{action_name}' not supported by {agent_name}."
                results.append(err)
                continue
                
            action_fn = getattr(agent, action_name)
            trace_id = f"{workflow_id}_{agent_name}_{action_name}"
            start_time = logging.time.time()
            self.telemetry.start_trace(trace_id)
            
            self.signals.emit("STEP_STARTED", {"agent": agent_name, "action": action_name, "args": processed_args}, sender="FleetManager")
            
            success = False
            max_retries = 2
            attempts = 0
            
            while not success and attempts <= max_retries:
                attempts += 1
                
                # Loop detection
                action_signature = f"{agent_name}.{action_name}({processed_args})"
                self.action_history.append(action_signature)
                if self.action_history.count(action_signature) >= 3:
                    logging.warning(f"LOOP DETECTED: {action_signature} repeated 3 times. Terminating step.")
                    self.signals.emit("LOOP_DETECTED", {"action": action_signature}, sender="FleetManager")
                    break

                try:
                    current_model = getattr(agent, "get_model", lambda: "default")()
                    logging.info(f"Fleet executing (Attempt {attempts}): {agent_name}.{action_name}({processed_args}) using model {current_model}")
                    
                    # Essential vs non-essential timeout (Phase 104)
                    is_essential = agent_name in self.agents.registry_configs
                    if is_essential:
                        res = action_fn(*processed_args)
                    else:
                        with ThreadPoolExecutor(max_workers=1) as executor:
                            future = executor.submit(action_fn, *processed_args)
                            try:
                                res = future.result(timeout=5.0)
                            except TimeoutError:
                                logging.warning(f"Workflow agent '{agent_name}' timed out after 5 seconds.")
                                raise Exception(f"Agent '{agent_name}' timed out after 5 seconds.")

                    # Scaling & RL feedback
                    duration = time.time() - start_time
                    self.scaling.record_metric(agent_name, duration)
                    self.rl_selector.update_stats(f"{agent_name}.{action_name}", success=True)
                    
                    success = True # Mark success to break loop
                    
                    # Try to extract token usage if the agent tracked it
                    token_info = getattr(agent, "_last_token_usage", {"input": 0, "output": 0, "model": current_model or "unknown"})
                    
                    self._record_success(res, workflow_id, agent_name, action_name, processed_args, token_info, trace_id, start_time)
                    results.append(f"### Results from {agent_name} ({action_name})\n{res}\n")
                    
                except Exception as e:
                    self.rl_selector.update_stats(f"{agent_name}.{action_name}", success=False)
                    logging.error(f"Fleet Execution Error (Attempt {attempts}): {e}")
                    error_msg = str(e)

                    # Trigger Self-Healing
                    if hasattr(self, 'self_healing'):
                        try:
                           heal_msg = self.self_healing.handle_failure(agent, action_name, e, {"args": processed_args})
                           logging.warning(f"Self-Healing: {heal_msg}")
                        except Exception as h_e:
                           logging.error(f"Self-healing mechanism failed: {h_e}")

                    if attempts <= max_retries:
                        current_model = getattr(agent, "get_model", lambda: "default")()
                        next_model = self.fallback_engine.get_fallback_model(current_model, failure_reason=error_msg)
                        
                        # Record Lesson for failure
                        self.global_context.record_lesson(
                            failure_context=f"{agent_name}.{action_name} failed with {error_msg}",
                            correction=f"Retry with {next_model}",
                            agent="FleetManager"
                        )
                        
                        if next_model and hasattr(agent, "set_model"):
                            logging.warning(f"Retrying {agent_name} with fallback model: {next_model}")
                            agent.set_model(next_model)
                            self.signals.emit("STEP_RETRYING", {"agent": agent_name, "fallback_model": next_model}, sender="FleetManager")
                            import threading
                            threading.Event().wait(timeout=1.0)
                            continue

                    self.state.errors.append(f"{agent_name}.{action_name}: {error_msg}")
                    results.append(f"### Error from {agent_name}\n{error_msg}\n")
                    self.telemetry.end_trace(trace_id, agent_name, action_name, status="error", metadata={"error": error_msg})
                    self.signals.emit("STEP_FAILED", {"agent": agent_name, "error": error_msg}, sender="FleetManager")
                    break

        duration = time.time() - start_time
        self.telemetry.trace_workflow(task, duration)
        self.telemetry.export_to_elk()
        self.signals.emit("WORKFLOW_COMPLETED", {"task": task, "workflow_id": workflow_id}, sender="FleetManager")
        return "# Fleet Workflow Summary\n\n" + "\n".join(results)


    def execute_with_consensus(self, task: str, primary_agent: str, secondary_agents: List[str]) -> Dict[str, Any]:
        """
        Executes a task across multiple agents and uses ByzantineConsensusAgent to pick the winner.
        Useful for high-integrity changes. (Phase 41)
        """
        logging.info(f"Fleet: Running consensus vote for task: {task[:50]}")
        
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
        result = self.byzantine_judge.run_committee_vote(task, proposals)
        
        # If success, broadcast lesson via Federated Knowledge
        if result["decision"] == "ACCEPTED":
            self.federated_knowledge.broadcast_lesson(
                lesson_id=f"consensus_{int(logging.time.time())}",
                lesson_data={
                    "agent": result["winner"],
                    "task_type": "high_integrity_code",
                    "success": True,
                    "fix": f"Consensus reached by {result['winner']} for {task[:30]}"
                }
            )
            
        return result


if __name__ == "__main__":
    # Test script for FleetManager
    logging.basicConfig(level=logging.INFO)
    root = Path("c:/DEV/PyAgent")
    fleet = FleetManager(str(root))
    
    fleet.register_agent("Knowledge", KnowledgeAgent, str(root / "src/classes/context/KnowledgeAgent.py"))
    fleet.register_agent("Security", SecurityGuardAgent, str(root / "src/classes/coder/SecurityGuardAgent.py"))
    
    workflow = [
        {"agent": "Knowledge", "action": "scan_workspace", "args": ["KnowledgeAgent"]},
        {"agent": "Security", "action": "improve_content", "args": ["password = os.environ.get('DB_PASSWORD')"]}
    ]
    
    report = fleet.execute_workflow("Initial Audit", workflow)
    print(report)
    print("\nTelemetry Summary:")
    print(json.dumps(fleet.telemetry.get_summary(), indent=2))
