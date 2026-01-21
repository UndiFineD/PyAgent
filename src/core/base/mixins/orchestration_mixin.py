#!/usr/bin/env python3
# Orchestration Mixin for BaseAgent
from typing import Any

class OrchestrationMixin:
    """Handles registry, tools, strategies, and distributed logging."""

    def __init__(self, **kwargs: Any) -> None:
        self.fleet: Any = None
        self._strategy: Any = None

        try:
            from src.infrastructure.orchestration.signals.signal_registry import SignalRegistry
            self.registry = SignalRegistry()
        except (ImportError, ValueError):
            self.registry = None

        try:
            from src.infrastructure.orchestration.system.tool_registry import ToolRegistry
            self.tool_registry = ToolRegistry()
        except (ImportError, ValueError):
            self.tool_registry = None

    @property
    def strategy(self) -> Any:
        if not hasattr(self, "_strategy") or self._strategy is None:
            try:
                from src.logic.strategies.direct_strategy import DirectStrategy
                self._strategy = DirectStrategy()
            except (ImportError, ModuleNotFoundError):
                self._strategy = None
        return self._strategy

    @strategy.setter
    def strategy(self, value: Any) -> None:
        self._strategy = value

    def set_strategy(self, strategy: Any) -> None:
        """Sets the execution strategy for the agent."""
        self._strategy = strategy

    def register_tools(self, registry: Any) -> None:
        if not registry:
            return
        # Assumes agent_logic_core and __class__ are available
        if hasattr(self, "agent_logic_core"):
            for method, cat, prio in self.agent_logic_core.collect_tools(self):
                registry.register_tool(self.__class__.__name__, method, cat, prio)

    def log_distributed(self, level: str, message: str, **kwargs: Any) -> None:
        """Publishes a log to the distributed logging system."""
        if hasattr(self, "fleet") and self.fleet:
            logging_agent = self.fleet.agents.get("Logging")
            if logging_agent:
                import asyncio
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(
                        logging_agent.broadcast_log(
                            level, self.__class__.__name__, message, kwargs
                        )
                    )
                except RuntimeError:
                    asyncio.run(
                        logging_agent.broadcast_log(
                            level, self.__class__.__name__, message, kwargs
                        )
                    )

    async def run_subagent(
        self, description: str, prompt: str, original_content: str = ""
    ) -> str:
        if hasattr(self, "quotas"):
            exceeded, reason = self.quotas.check_quotas()
            if exceeded:
                from src.core.base.base_exceptions import CycleInterrupt
                raise CycleInterrupt(reason)

        try:
            from src.infrastructure.backend import execution_engine as ab
        except ImportError:
            import sys
            from pathlib import Path
            sys.path.append(str(Path(__file__).parent.parent.parent.parent))
            from src.infrastructure.backend import execution_engine as ab

        import asyncio
        result: str | None = await asyncio.to_thread(
            ab.run_subagent, description, prompt, original_content
        )

        if hasattr(self, "quotas") and result:
             self.quotas.update_usage(len(prompt) // 4, len(result) // 4)

        if result is None:
            if original_content:
                return original_content
            if hasattr(self, "_get_fallback_response"):
                return self._get_fallback_response()
            return original_content
        return result

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Improve content using a subagent (respected strategy if set)."""
        actual_path = None
        if target_file:
            from pathlib import Path
            actual_path = Path(target_file)
        elif hasattr(self, "file_path"):
            actual_path = self.file_path

        description = (
            f"Improve {actual_path.name}"
            if actual_path
            else "Improve content"
        )
        original = getattr(self, "previous_content", "")

        curr_strategy = self.strategy
        if curr_strategy:

            async def backend_call(
                p: str,
                sp: str | None = None,
                h: list[dict[str, str]] | None = None,
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
        try:
            from src.infrastructure import backend as ab
        except ImportError:
            return {}
        return ab.get_backend_status()

    @staticmethod
    def describe_backends() -> str:
        try:
            from src.infrastructure import backend as ab
        except ImportError:
            return "Backends unavailable"
        return ab.describe_backends()

    async def delegate_to(self, agent_type: str, prompt: str, target_file: str | None = None) -> str:
        """
        Synaptic Delegation: Hands off a sub-task to a specialized agent.
        Supports both fleet-managed agents and dynamic on-demand instantiation.
        """
        import logging
        from pathlib import Path
        import asyncio

        logging.info(f"[{self.__class__.__name__}] Delegating task to {agent_type} (Target: {target_file})")

        # 1. Attempt delegation via Fleet Manager (if attached)
        if hasattr(self, "fleet") and self.fleet:
            try:
                # FleetManager.agents is a LazyAgentMap
                if agent_type in self.fleet.agents:
                    sub_agent = self.fleet.agents[agent_type]
                    
                    # Log the delegation event
                    self.log_distributed("INFO", f"Delegated to fleet agent: {agent_type}", target=target_file)
                    
                    # Execute with explicit target_file (Phase 317 thread-safety)
                    res = sub_agent.improve_content(prompt, target_file=target_file)
                    if asyncio.iscoroutine(res):
                        return await res
                    return res
            except Exception as e:
                logging.warning(f"Fleet delegation failed for {agent_type}: {e}")

        # 2. Dynamic Import Fallback (via AgentRegistry)
        try:
            from src.infrastructure.fleet.agent_registry import AgentRegistry
            from src.core.base.agent_core import BaseCore
            
            ws_root = getattr(self, "_workspace_root", None) or Path(BaseCore.detect_workspace_root(Path.cwd()))
            
            # Use the registry to get the agent map
            agent_map = AgentRegistry.get_agent_map(ws_root, fleet_instance=getattr(self, "fleet", None))
            
            if agent_type in agent_map:
                sub_agent = agent_map[agent_type]
                
                self.log_distributed("INFO", f"Delegated to registry agent: {agent_type}", target=target_file)
                
                # Execute with explicit target_file
                res = sub_agent.improve_content(prompt, target_file=target_file)
                if asyncio.iscoroutine(res):
                    return await res
                return res

        except Exception as e:
            logging.error(f"Registry delegation failed for {agent_type}: {e}")
            return f"Error: Registry lookup of {agent_type} failed. {str(e)}"

        return f"Error: Agent {agent_type} not found in system catalogs."
