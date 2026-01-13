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

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import time
from typing import Dict, List, Any, TYPE_CHECKING
from .WorkflowState import WorkflowState

__version__ = VERSION

if TYPE_CHECKING:
    from .FleetManager import FleetManager

class FleetExecutionCore:
    """Handles core workflow execution and task reliability logic for the Fleet."""

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet

    async def execute_reliable_task(self, task: str) -> str:
        """Executes a task using the 7-phase inner loop and linguistic articulation."""
        current_model = "internal_ai"
        try:
            if hasattr(self.fleet, 'router_model'):
                current_model = await self.fleet.router_model.determine_optimal_provider(task)
            logging.info(f"Fleet selected model '{current_model}' for task.")
        except Exception:
            logging.debug("Defaulting to internal_ai model.")

        try:
            # Phase 152: Transition core logic to async
            technical_report = await self.fleet.structured_orchestrator.execute_task(task)
            res = await self.fleet.linguist.articulate_results(technical_report, task)
            await self.fleet._record_success(task, res, current_model)
            return res
        except Exception as e:
            await self.fleet._record_failure(task, str(e), current_model)
            logging.error(f"Fleet failure: {e}")
            fallback_model = self.fleet.fallback_engine.get_fallback_model(current_model, str(e))
            if fallback_model and fallback_model != current_model:
                logging.warning(f"Self-Healing: Retrying with fallback model {fallback_model}...")
                try:
                    technical_report = await self.fleet.structured_orchestrator.execute_task(task)
                    return await self.fleet.linguist.articulate_results(technical_report, task)
                except Exception as e2:
                    logging.critical(f"Self-Healing: Fallback also failed: {e2}")
            raise

    async def execute_workflow(self, task: str, workflow_steps: List[Dict[str, Any]]) -> str:
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
            
            # Variable processing
            processed_args = []
            for arg in args:
                if isinstance(arg, str) and arg.startswith("$"):
                    var_name = arg[1:]
                    processed_args.append(self.fleet.state.get(var_name, arg))
                else:
                    processed_args.append(arg)

            agent = self.fleet.agents.get(agent_name)
            if not agent:
                err = f"Error: Agent '{agent_name}' not found."
                results.append(err)
                self.fleet.signals.emit("AGENT_NOT_FOUND", {"agent": agent_name, "step": step}, sender="FleetManager")
                continue
                
            action_fn = getattr(agent, action_name, None)
            if not action_fn:
                err = f"Error: Action '{action_name}' not supported by {agent_name}."
                results.append(err)
                continue

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
                    import asyncio
                    current_model = getattr(agent, "get_model", lambda: "default")()
                    logging.info(f"Fleet (Attempt {attempts}): {agent_name}.{action_name}({processed_args}) using {current_model}")
                    
                    if asyncio.iscoroutinefunction(action_fn):
                        res = await action_fn(*processed_args)
                    else:
                        loop = asyncio.get_running_loop()
                        res = await loop.run_in_executor(None, action_fn, *processed_args)

                    duration = time.time() - start_time
                    self.fleet.scaling.record_metric(agent_name, duration)
                    rl = self.fleet.rl_selector
                    if rl:
                        rl.update_stats(f"{agent_name}.{action_name}", success=True)
                    
                    success = True
                    token_info = getattr(agent, "_last_token_usage", {"input": 0, "output": 0, "model": current_model or "unknown"})
                    await self.fleet._record_success(res, workflow_id, agent_name, action_name, processed_args, token_info, trace_id, start_time)
                    results.append(f"### Results from {agent_name} ({action_name})\n{res}\n")
                    self.fleet.telemetry.end_trace(trace_id, agent_name, action_name, status="success")
                except Exception as e:
                    rl = self.fleet.rl_selector
                    if rl:
                        rl.update_stats(f"{agent_name}.{action_name}", success=False)
                    logging.error(f"Fleet Execution Error (Attempt {attempts}): {e}")
                    error_msg = str(e)

                    if attempts <= max_retries:
                        await self.fleet._record_failure(f"{agent_name}.{action_name}", error_msg, "unknown")
                        await asyncio.sleep(1.0)
                        continue

                    self.fleet.state.errors.append(f"{agent_name}.{action_name}: {error_msg}")
                    results.append(f"### Error from {agent_name}\n{error_msg}\n")
                    self.fleet.telemetry.end_trace(trace_id, agent_name, action_name, status="error", metadata={"error": error_msg})
                    break

        return "# Fleet Workflow Summary\n\n" + "\n".join(results)