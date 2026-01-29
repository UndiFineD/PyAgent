#!/usr/bin/env python3
"""
Module: orchestration_mixin
Provides orchestration and context propagation mixin for PyAgent agents.
"""
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

"""Orchestration Mixin for BaseAgent."""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Any

from src.infrastructure.swarm.fleet.agent_registry import LazyAgentMap


class OrchestrationMixin:
    """Handles registry, tools, strategies, and distributed logging."""

    def __init__(self, **_kwargs: Any) -> None:
        self.fleet: Any = None
        self._strategy: Any = None

        try:
            # pylint: disable=import-outside-toplevel
            from src.infrastructure.swarm.orchestration.signals.signal_registry import \
                SignalRegistry

            self.registry = SignalRegistry()
        except (ImportError, ValueError):
            self.registry = None

        try:
            # pylint: disable=import-outside-toplevel
            from src.infrastructure.swarm.orchestration.system.tool_registry import \
                ToolRegistry

            self.tool_registry = ToolRegistry()
        except (ImportError, ValueError):
            self.tool_registry = None

    @property
    def strategy(self) -> Any:
        """Access the execution strategy."""
        if not hasattr(self, "_strategy") or self._strategy is None:
            try:
                # pylint: disable=import-outside-toplevel
                from src.logic.strategies.direct_strategy import DirectStrategy

                self._strategy = DirectStrategy()
            except (ImportError, ModuleNotFoundError):
                self._strategy = None
        return self._strategy

    @strategy.setter
    def strategy(self, value: Any) -> None:
        """Set the execution strategy."""
        self._strategy = value

    def set_strategy(self, strategy: Any) -> None:
        """Sets the execution strategy for the agent."""
        self._strategy = strategy

    def register_tools(self, registry: Any) -> None:
        """Register agent tools with a registry."""
        if not registry:
            return
        # Assumes agent_logic_core and __class__ are available
        if hasattr(self, "agent_logic_core"):
            for method, cat, prio in getattr(self, "agent_logic_core").collect_tools(self):
                registry.register_tool(self.__class__.__name__, method, cat, prio)

    def log_distributed(self, level: str, message: str, **kwargs: Any) -> None:
        """Publishes a log to the distributed logging system."""
        if hasattr(self, "fleet") and getattr(self, "fleet"):
            logging_agent = getattr(self, "fleet").agents.get("Logging")
            if logging_agent:
                try:
                    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
                    loop.create_task(logging_agent.broadcast_log(level, self.__class__.__name__, message, kwargs))
                except RuntimeError:
                    asyncio.run(logging_agent.broadcast_log(level, self.__class__.__name__, message, kwargs))

    async def run_subagent(self, description: str, prompt: str, original_content: str = "") -> str:
        """Run a subagent to handle a task."""
        if hasattr(self, "quotas"):
            exceeded, reason = getattr(self, "quotas").check_quotas()
            if exceeded:
                # pylint: disable=import-outside-toplevel
                from src.core.base.common.base_exceptions import CycleInterrupt

                raise CycleInterrupt(reason)

        try:
            # pylint: disable=import-outside-toplevel
            from src.infrastructure.compute.backend import \
                execution_engine as ab
        except ImportError:
            sys.path.append(str(Path(__file__).parent.parent.parent.parent))
            # pylint: disable=import-outside-toplevel
            from src.infrastructure.compute.backend import \
                execution_engine as ab

        result: str | None = await asyncio.to_thread(ab.run_subagent, description, prompt, original_content)

        if hasattr(self, "quotas") and result:
            getattr(self, "quotas").update_usage(len(prompt) // 4, len(result) // 4)

        if result is None:
            if original_content:
                return original_content
            if hasattr(self, "_get_fallback_response"):
                return getattr(self, "_get_fallback_response")()
            return original_content
        return result

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Improve content using a subagent (respected strategy if set)."""
        actual_path = None
        if target_file:
            actual_path = Path(target_file)
        elif hasattr(self, "file_path"):
            actual_path = getattr(self, "file_path")

        description: str = f"Improve {actual_path.name}" if actual_path else "Improve content"
        original: Any | str = getattr(self, "previous_content", "")

        curr_strategy = self.strategy
        if curr_strategy:

            async def backend_call(
                p: str,
                _sp: str | None = None,
                _h: list[dict[str, str]] | None = None,
            ) -> str:
                # We ignore sp and h for now as run_subagent doesn't support them yet
                # but they could be injected into the prompt if needed.
                return await self.run_subagent(description, p, original)

            return await curr_strategy.execute(
                prompt,
                original,
                backend_call,
                system_prompt=getattr(self, "_system_prompt", None),
            )

        return await self.run_subagent(description, prompt, original)

    @staticmethod
    def get_backend_status() -> dict[str, Any]:
        """Get the status of the execution backend."""
        try:
            # pylint: disable=import-outside-toplevel
            from src.infrastructure import backend as ab
        except ImportError:
            return {}
        return ab.get_backend_status()

    @staticmethod
    def describe_backends() -> str:
        """Return a description of available backends."""
        try:
            # pylint: disable=import-outside-toplevel
            from src.infrastructure import backend as ab
        except ImportError:
            return "Backends unavailable"
        return ab.describe_backends()

    async def delegate_to(self, agent_type: str, prompt: str, target_file: str | None = None) -> str:
        """
        Synaptic Delegation: Hands off a sub-task to a specialized agent.
        Supports both fleet-managed agents and dynamic on-demand instantiation.
        """
        logging.info("[%s] Delegating task to %s (Target: %s)", self.__class__.__name__, agent_type, target_file)

        # Prepare context for delegation (Phase 259)
        next_context = self._prepare_delegation_context()

        # Try fleet delegation first
        result = await self._try_fleet_delegation(agent_type, prompt, target_file, next_context)
        if result is not None:
            return result

        # Fallback to registry delegation
        result = await self._try_registry_delegation(agent_type, prompt, target_file, next_context)
        if result is not None:
            return result

        return f"Error: Agent {agent_type} not found in system catalogs."

    def _prepare_delegation_context(self) -> Any | None:
        """Prepare context for delegation propagation."""
        if not hasattr(self, "context") or not self.context:
            return None

        try:
            if hasattr(self.context, "next_level"):
                return self.context.next_level(self.__class__.__name__)
            else:
                return self.context
        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.warning("Failed to propagate context: %s", e)
            return None

    async def _try_fleet_delegation(self, agent_type: str, prompt: str, target_file: str | None, context: Any | None) -> str | None:
        """Attempt delegation via Fleet Manager."""
        if not hasattr(self, "fleet") or not getattr(self, "fleet"):
            return None

        try:
            # FleetManager.agents is a LazyAgentMap
            if agent_type in getattr(self, "fleet").agents:
                sub_agent = getattr(self, "fleet").agents[agent_type]

                # Propagate context
                if context and hasattr(sub_agent, "context"):
                    sub_agent.context = context

                # Log the delegation event
                self.log_distributed("INFO", f"Delegated to fleet agent: {agent_type}", target=target_file)

                # Execute with explicit target_file (Phase 317 thread-safety)
                res = sub_agent.improve_content(prompt, target_file=target_file)
                if asyncio.iscoroutine(res):
                    return await res
                return res
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.warning("Fleet delegation failed for %s: %s", agent_type, e)

        return None

    async def _try_registry_delegation(self, agent_type: str, prompt: str, target_file: str | None, context: Any | None) -> str | None:
        """Attempt delegation via AgentRegistry fallback."""
        try:
            # pylint: disable=import-outside-toplevel
            from src.core.base.lifecycle.agent_core import BaseCore
            from src.infrastructure.swarm.fleet.agent_registry import AgentRegistry

            ws_root: Any | Path = getattr(self, "_workspace_root", None) or Path(BaseCore.detect_workspace_root(Path.cwd()))

            # Use the registry to get the agent map
            agent_map: LazyAgentMap = AgentRegistry.get_agent_map(ws_root, fleet_instance=getattr(self, "fleet", None))

            if agent_type in agent_map:
                sub_agent = agent_map[agent_type]

                # Propagate context
                if context and hasattr(sub_agent, "context"):
                    sub_agent.context = context

                self.log_distributed("INFO", f"Delegated to registry agent: {agent_type}", target=target_file)

                # Execute with explicit target_file
                res = sub_agent.improve_content(prompt, target_file=target_file)
                if asyncio.iscoroutine(res):
                    return await res
                return res

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error("Registry delegation failed for %s: %s", agent_type, e)
            return f"Error: Registry lookup of {agent_type} failed. {str(e)}"

        return None
