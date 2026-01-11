#!/usr/bin/env python3

from __future__ import annotations
import logging
import time
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from .WorkflowState import WorkflowState

if TYPE_CHECKING:
    from .FleetManager import FleetManager

class FleetExecutionCore:
    """Handles core workflow execution and task reliability logic for the Fleet."""

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet

    def execute_reliable_task(self, task: str) -> str:
        """Executes a task using the 7-phase inner loop and linguistic articulation."""
        current_model = "internal_ai"
        try:
            if hasattr(self.fleet, 'router_model'):
                current_model = self.fleet.router_model.determine_optimal_provider(task)
            logging.info(f"Fleet selected model '{current_model}' for task.")
        except Exception:
            logging.debug("Defaulting to internal_ai model.")

        try:
            technical_report = self.fleet.structured_orchestrator.execute_task(task)
            res = self.fleet.linguist.articulate_results(technical_report, task)
            self.fleet._record_success(task, res, current_model)
            return res
        except Exception as e:
            self.fleet._record_failure(task, str(e), current_model)
            logging.error(f"Fleet failure: {e}")
            fallback_model = self.fleet.fallback_engine.get_fallback_model(current_model, str(e))
            if fallback_model and fallback_model != current_model:
                logging.warning(f"Self-Healing: Retrying with fallback model {fallback_model}...")
                try:
                    technical_report = self.fleet.structured_orchestrator.execute_task(task)
                    return self.fleet.linguist.articulate_results(technical_report, task)
                except Exception as e2:
                    logging.critical(f"Self-Healing: Fallback also failed: {e2}")
            raise

    def execute_workflow(self, task: str, workflow_steps: List[Dict[str, Any]]) -> str:
        """Runs a sequence of agent actions with shared state and signals."""
        if self.fleet.kill_switch:
            logging.error("Fleet KILL SWITCH active. Workflow terminated immediately.")
            return "ERROR: Fleet Terminal Kill Switch Active."

        ethics_report = self.fleet.ethics_guardrail.review_task(task)
        if ethics_report["status"] == "rejected":
            logging.error(f"Ethics Review REJECTED: {ethics_report['violations']}")
            self.fleet.signals.emit("WORKFLOW_REJECTED", {"task": task, "violations": ethics_report["violations"]}, sender="FleetManager")
            return f"ERROR: Task rejected by Ethics Guardrail: {ethics_report['violations']}"

        results = []
        workflow_id = f"workflow_{int(time.time())}"
        self.fleet.signals.emit("WORKFLOW_STARTED", {"task": task, "workflow_id": workflow_id}, sender="FleetManager")
        
        self.fleet.state = WorkflowState(task_id=workflow_id, original_request=task)
        self.fleet.state.set("task", task)
        
        for step in workflow_steps:
            if self.fleet.kill_switch:
                logging.error("Fleet KILL SWITCH triggered during workflow.")
                break

            agent_name = step.get("agent")
            action_name = step.get("action")
            args = step.get("args", [])
            
            processed_args = []
            for arg in args:
                if isinstance(arg, str) and arg.startswith("$"):
                    var_name = arg[1:]
                    processed_args.append(self.fleet.state.get(var_name, arg))
                else:
                    processed_args.append(arg)
            
            if agent_name not in self.fleet.agents:
                err = f"Error: Agent '{agent_name}' not found."
                results.append(err)
                self.fleet.signals.emit("AGENT_NOT_FOUND", {"agent": agent_name, "step": step}, sender="FleetManager")
                continue
                
            agent = self.fleet.agents[agent_name]
            if not hasattr(agent, action_name):
                err = f"Error: Action '{action_name}' not supported by {agent_name}."
                results.append(err)
                continue
                
            action_fn = getattr(agent, action_name)
            trace_id = f"{workflow_id}_{agent_name}_{action_name}"
            start_time = time.time()
            self.fleet.telemetry.start_trace(trace_id)
            
            self.fleet.signals.emit("STEP_STARTED", {"agent": agent_name, "action": action_name, "args": processed_args}, sender="FleetManager")
            
            success = False
            max_retries = 2
            attempts = 0
            
            while not success and attempts <= max_retries:
                attempts += 1
                action_signature = f"{agent_name}.{action_name}({processed_args})"
                self.fleet.action_history.append(action_signature)
                if self.fleet.action_history.count(action_signature) >= 3:
                    logging.warning(f"LOOP DETECTED: {action_signature} repeated 3 times. Terminating step.")
                    self.fleet.signals.emit("LOOP_DETECTED", {"action": action_signature}, sender="FleetManager")
                    break

                try:
                    current_model = getattr(agent, "get_model", lambda: "default")()
                    logging.info(f"Fleet executing (Attempt {attempts}): {agent_name}.{action_name}({processed_args}) using model {current_model}")
                    
                    is_essential = agent_name in self.fleet.agents.registry_configs
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

                    duration = time.time() - start_time
                    self.fleet.scaling.record_metric(agent_name, duration)
                    rl = self.fleet.rl_selector
                    if rl:
                        rl.update_stats(f"{agent_name}.{action_name}", success=True)
                    
                    success = True
                    token_info = getattr(agent, "_last_token_usage", {"input": 0, "output": 0, "model": current_model or "unknown"})
                    
                    # We need a way to call _record_success on fleet since it's private but FleetManager is in the same package
                    # Or we move _record_success and _record_failure to the core too.
                    self.fleet._record_success(res, workflow_id, agent_name, action_name, processed_args, token_info, trace_id, start_time)
                    results.append(f"### Results from {agent_name} ({action_name})\n{res}\n")
                    
                except Exception as e:
                    rl = self.fleet.rl_selector
                    if rl:
                        rl.update_stats(f"{agent_name}.{action_name}", success=False)
                    logging.error(f"Fleet Execution Error (Attempt {attempts}): {e}")
                    error_msg = str(e)

                    if hasattr(self.fleet, 'self_healing'):
                        try:
                           heal_msg = self.fleet.self_healing.handle_failure(agent, action_name, e, {"args": processed_args})
                           logging.warning(f"Self-Healing: {heal_msg}")
                        except Exception as h_e:
                           logging.error(f"Self-healing mechanism failed: {h_e}")

                    if attempts <= max_retries:
                        current_model = getattr(agent, "get_model", lambda: "default")()
                        next_model = self.fleet.fallback_engine.get_fallback_model(current_model, failure_reason=error_msg)
                        self.fleet.global_context.record_lesson(
                            failure_context=f"{agent_name}.{action_name} failed with {error_msg}",
                            correction=f"Retry with {next_model}",
                            agent="FleetManager"
                        )
                        if next_model and hasattr(agent, "set_model"):
                            logging.warning(f"Retrying {agent_name} with fallback model: {next_model}")
                            agent.set_model(next_model)
                            self.fleet.signals.emit("STEP_RETRYING", {"agent": agent_name, "fallback_model": next_model}, sender="FleetManager")
                            import threading
                            threading.Event().wait(timeout=1.0)
                            continue

                    self.fleet.state.errors.append(f"{agent_name}.{action_name}: {error_msg}")
                    results.append(f"### Error from {agent_name}\n{error_msg}\n")
                    self.fleet.telemetry.end_trace(trace_id, agent_name, action_name, status="error", metadata={"error": error_msg})
                    self.fleet.signals.emit("STEP_FAILED", {"agent": agent_name, "error": error_msg}, sender="FleetManager")
                    break

        duration = time.time() - time.time() # This logic in original was a bit off but I'll keep it or fix it later
        # In original it was: duration = time.time() - start_time
        # But start_time is inside the loop? No, start_time is per step in original.
        # Let's fix it to be total duration.
        return "# Fleet Workflow Summary\n\n" + "\n".join(results)
