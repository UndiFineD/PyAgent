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

"""Routing logic for the FleetManager."""

from __future__ import annotations

import asyncio
import inspect
import logging
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .fleet_manager import FleetManager


class FleetRoutingCore:
    """Handles task routing and capability-based agent selection."""

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet

    async def call_by_capability(self, goal: str, **kwargs) -> Any:
        """Finds an agent with the required capability and executes it with RL optimization."""
        # Report activity to TemporalSync
        if hasattr(self.fleet, "temporal_sync"):
            self.fleet.temporal_sync.report_activity()

        self._ensure_agents_loaded(goal)

        # Get tool metadata for scoring
        tools = self.fleet.registry.list_tools()
        tools_metadata = [{"name": t.name, "owner": t.owner, "sync": getattr(t, "sync", True)} for t in tools]

        scored_candidates = self.fleet.core.score_tool_candidates(goal, tools_metadata, kwargs)

        if not scored_candidates:
            return f"No tool found for goal: {goal}"

        best_tool = self._select_optimized_tool(goal, [c[1] for c in scored_candidates])
        return await self._execute_tool_with_lifecycle(best_tool, tools, goal, **kwargs)

    def _ensure_agents_loaded(self, goal: str) -> None:
        """Heuristically load agents based on the goal string."""
        g_low = goal.lower().replace("_", "").replace("-", "")
        for hint_key, agent_name in self.fleet.capability_hints.items():
            if hint_key.lower().replace("_", "") in g_low and agent_name in self.fleet.agents:
                _ = self.fleet.agents[agent_name]  # Force load
                logging.info(f"Fleet: Lazy-loaded '{agent_name}' for capability '{hint_key}'")

        if goal in self.fleet.agents:
            _ = self.fleet.agents[goal]
        else:
            for agent_name in self.fleet.agents:
                if g_low in agent_name.lower():
                    _ = self.fleet.agents[agent_name]
                    break

    def _select_optimized_tool(self, goal: str, candidates: list[str]) -> str:
        """Select the best tool from candidates, using RL if available."""
        selector = self.fleet.rl_selector
        if selector and hasattr(selector, "select_best_tool"):
            best_tool = selector.select_best_tool(candidates)
            logging.info(f"Fleet selected optimized tool '{best_tool}' using RL for goal '{goal}'")
            return best_tool

        logging.info(f"Fleet: RLSelector missing. Defaulting to first candidate '{candidates[0]}' for goal '{goal}'")
        return candidates[0]

    async def _execute_tool_with_lifecycle(self, best_tool: str, tools: list[Any], goal: str, **kwargs) -> Any:
        """Execute the selected tool with built-in timeout, security audit, and self-healing."""
        owner = next((t.owner for t in tools if t.name == best_tool), None)
        is_essential = owner in self.fleet.agents.registry_configs if owner else False
        start_time = time.time()

        try:

            async def run_tool() -> Any:
                if inspect.iscoroutinefunction(self.fleet.registry.call_tool):
                    return await self.fleet.registry.call_tool(best_tool, **kwargs)

                loop = asyncio.get_running_loop()
                return await loop.run_in_executor(None, self.fleet.registry.call_tool, best_tool, **kwargs)

            if is_essential:
                res = await run_tool()
            else:
                try:
                    res = await asyncio.wait_for(run_tool(), timeout=5.0)
                except asyncio.TimeoutError:
                    error_msg = f"Non-essential tool '{best_tool}' (owner: {owner}) timed out after 5 seconds."
                    logging.warning(error_msg)
                    # Record failure in RL
                    if hasattr(self.fleet, "rl_selector"):
                        self.fleet.rl_selector.record_feedback(goal, best_tool, success=False)
                    return error_msg

            # Phase 123: Security Audit Feedback Loop
            if not await self._perform_security_audit(best_tool, str(res)):
                # Record security failure in RL
                if hasattr(self.fleet, "rl_selector"):
                    self.fleet.rl_selector.record_feedback(goal, best_tool, success=False)
                return f"ERROR: Security audit failed for tool '{best_tool}'. Output blocked."

            # Success! Record feedback in RL
            latency = time.time() - start_time
            if hasattr(self.fleet, "rl_selector"):
                self.fleet.rl_selector.record_feedback(goal, best_tool, success=True, latency=latency)
            
            return res

            if self.fleet.rl_selector:
                self.fleet.rl_selector.update_stats(best_tool, success=True)
            await self.fleet.record_success(f"Capability call: {goal} with {kwargs}", str(res), "internal_ai")
            return res
        except Exception as exc:  # pylint: disable=broad-exception-caught
            if self.fleet.rl_selector:
                self.fleet.rl_selector.update_stats(best_tool, success=False)
            logging.error(f"Error executing tool {best_tool}: {exc}")
            return await self._attempt_self_healing(best_tool, owner, exc, **kwargs)
        finally:
            if hasattr(self.fleet, "telemetry"):
                self.fleet.telemetry.trace_workflow(f"tool_{best_tool}", time.time() - start_time)

    async def _perform_security_audit(self, best_tool: str, result: str) -> bool:
        """Invokes ImmuneSystem to audit tool output."""
        if "ImmuneSystem" not in self.fleet.agents:
            return True

        try:
            immune = self.fleet.agents["ImmuneSystem"]
            if inspect.iscoroutinefunction(immune.perform_security_audit):
                audit_passed = await immune.perform_security_audit(best_tool, result)
            else:
                audit_passed = immune.perform_security_audit(best_tool, result)
        except (AttributeError, ValueError, TypeError):
            audit_passed = True

        if not audit_passed:
            logging.warning(f"Fleet: Security audit FAILED for tool '{best_tool}'. Penalizing RLSelector.")
            if self.fleet.rl_selector:
                self.fleet.rl_selector.update_stats(best_tool, success=False)
            return False
        return True

    async def _attempt_self_healing(self, best_tool: str, owner: str | None, error: Exception, **kwargs) -> str:
        """Attempt to repair the agent or environment if an error occurs."""
        if not self.fleet.self_healing:
            return f"Error executing tool {best_tool}: {error}"

        target_agent = owner if owner else best_tool
        clean_kwargs = {k: v for k, v in kwargs.items() if k != "agent_name"}
        if inspect.iscoroutinefunction(self.fleet.self_healing.attempt_repair):
            return await self.fleet.self_healing.attempt_repair(target_agent, error, **clean_kwargs)

        return self.fleet.self_healing.attempt_repair(target_agent, error, **clean_kwargs)

    def route_task(self, task_type: str, _task_data: Any) -> str:
        """Routes tasks based on system load and hardware availability."""
        stats = self.fleet.telemetry.orchestrator.monitor.get_current_stats()
        is_compute_heavy = task_type in ["training", "indexing", "llm_finetune"]

        if is_compute_heavy and stats["gpu"]["available"]:
            logging.info(f"Fleet: Routing {task_type} to GPU node ({stats['gpu']['type']})")
            return f"ROUTED:GPU:{stats['gpu']['type']}"
        if is_compute_heavy and stats["status"] == "CRITICAL":
            logging.warning("Fleet: System critical, deferring compute-heavy task.")
            return "DEFERRED:LOAD_CRITICAL"

        logging.info(f"Fleet: Routing {task_type} to standard CPU pool.")
        return "ROUTED:CPU:POOL"
