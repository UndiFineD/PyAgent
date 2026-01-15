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
import logging
import time
from typing import Any, TYPE_CHECKING
import asyncio

if TYPE_CHECKING:
    from .FleetManager import FleetManager




class FleetRoutingCore:
    """Handles task routing and capability-based agent selection."""

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet

    async def call_by_capability(self, goal: str, **kwargs) -> str:
        """Finds an agent with the required capability and executes it with RL optimization."""
        # Report activity to TemporalSync
        if hasattr(self.fleet, 'temporal_sync'):
            self.fleet.temporal_sync.report_activity()

        g_low = goal.lower()

        # New: Capability Hint Lookup
        for hint_key, agent_name in self.fleet._capability_hints.items():
            if hint_key in g_low and agent_name in self.fleet.agents:
                _ = self.fleet.agents[agent_name]  # Force load
                logging.info(f"Fleet: Lazy-loaded '{agent_name}' for capability '{hint_key}'")

        # New: Auto-instantiate agent if goal matches agent name
        if goal in self.fleet.agents:
            _ = self.fleet.agents[goal]  # Access triggers instantiation and tool registration
        else:
            # Check if any agent name contains the goal
            for agent_name in self.fleet.agents:
                if g_low in agent_name.lower():
                    _ = self.fleet.agents[agent_name]
                    break

        # Get tool metadata for scoring
        tools = self.fleet.registry.list_tools()
        tools_metadata = []
        for t in tools:
            tools_metadata.append({
                "name": t.name,
                "owner": t.owner,
                "sync": getattr(t, 'sync', True)
            })

        scored_candidates = self.fleet.core.score_tool_candidates(goal, tools_metadata, kwargs)

        if not scored_candidates:
            return f"No tool found for goal: {goal}"

        candidates = [c[1] for c in scored_candidates]

        selector = self.fleet.rl_selector
        if selector and hasattr(selector, "select_best_tool"):
            best_tool = selector.select_best_tool(candidates)
            logging.info(f"Fleet selected optimized tool '{best_tool}' using RL for goal '{goal}'")
        else:
            best_tool = candidates[0]
            logging.info(f"Fleet: RLSelector missing or incompatible. Defaulting to first candidate '{best_tool}' for goal '{goal}'")

        owner = next((t.owner for t in tools if t.name == best_tool), None)
        is_essential = owner in self.fleet.agents.registry_configs if owner else False

        start_time = time.time()
        try:
            async def run_tool() -> str:
                if asyncio.iscoroutinefunction(self.fleet.registry.call_tool):
                    return await self.fleet.registry.call_tool(best_tool, **kwargs)
                else:
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
                    return error_msg

            # Phase 123: Security Audit Feedback Loop
            audit_passed = True
            if "ImmuneSystem" in self.fleet.agents:
                try:
                    immune = self.fleet.agents["ImmuneSystem"]
                    if asyncio.iscoroutinefunction(immune.perform_security_audit):
                        audit_passed = await immune.perform_security_audit(best_tool, str(res))
                    else:
                        audit_passed = immune.perform_security_audit(best_tool, str(res))
                except (AttributeError, ValueError, TypeError):
                    pass

            if not audit_passed:
                logging.warning(f"Fleet: Security audit FAILED for tool '{best_tool}'. Penalizing RLSelector.")
                if self.fleet.rl_selector:
                    self.fleet.rl_selector.update_stats(best_tool, success=False)
                return f"ERROR: Security audit failed for tool '{best_tool}'. Output blocked."

            if self.fleet.rl_selector:
                self.fleet.rl_selector.update_stats(best_tool, success=True)
            await self.fleet._record_success(f"Capability call: {goal} with {kwargs}", str(res), "internal_ai")
            return res
        except Exception as e:
            if self.fleet.rl_selector:
                self.fleet.rl_selector.update_stats(best_tool, success=False)
            logging.error(f"Error executing tool {best_tool}: {e}")
            if self.fleet.self_healing:
                target_agent = owner if owner else best_tool
                clean_kwargs = {k: v for k, v in kwargs.items() if k != "agent_name"}
                if asyncio.iscoroutinefunction(self.fleet.self_healing.attempt_repair):
                    return await self.fleet.self_healing.attempt_repair(target_agent, e, **clean_kwargs)
                else:
                    return self.fleet.self_healing.attempt_repair(target_agent, e, **clean_kwargs)
            return f"Error executing tool {best_tool}: {e}"
        finally:
            if hasattr(self.fleet, 'telemetry'):
                self.fleet.telemetry.trace_workflow(f"tool_{best_tool}", time.time() - start_time)

    def route_task(self, task_type: str, task_data: Any) -> str:
        """Routes tasks based on system load and hardware availability."""
        stats = self.fleet.telemetry.orchestrator.monitor.get_current_stats()
        is_compute_heavy = task_type in ["training", "indexing", "llm_finetune"]

        if is_compute_heavy and stats["gpu"]["available"]:
            logging.info(f"Fleet: Routing {task_type} to GPU node ({stats['gpu']['type']})")
            return f"ROUTED:GPU:{stats['gpu']['type']}"
        elif is_compute_heavy and stats["status"] == "CRITICAL":
            logging.warning("Fleet: System critical, deferring compute-heavy task.")
            return "DEFERRED:LOAD_CRITICAL"

        logging.info(f"Fleet: Routing {task_type} to standard CPU pool.")
        return "ROUTED:CPU:POOL"
