#!/usr/bin/env python3
# Orchestration Mixin for BaseAgent
from typing import Any

class OrchestrationMixin:
    """Handles registry, tools, strategies, and distributed logging."""

    def __init__(self, **kwargs: Any) -> None:
        self.fleet: Any = None
        self._strategy: Any = None

        try:
            from src.infrastructure.orchestration.signals.SignalRegistry import SignalRegistry
            self.registry = SignalRegistry()
        except (ImportError, ValueError):
            self.registry = None

        try:
            from src.infrastructure.orchestration.system.ToolRegistry import ToolRegistry
            self.tool_registry = ToolRegistry()
        except (ImportError, ValueError):
            self.tool_registry = None

    @property
    def strategy(self) -> Any:
        if not hasattr(self, "_strategy") or self._strategy is None:
            try:
                from src.logic.strategies.DirectStrategy import DirectStrategy
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
                from src.core.base.BaseExceptions import CycleInterrupt
                raise CycleInterrupt(reason)

        try:
            from src.infrastructure.backend import ExecutionEngine as ab
        except ImportError:
            import sys
            from pathlib import Path
            sys.path.append(str(Path(__file__).parent.parent.parent.parent))
            from src.infrastructure.backend import ExecutionEngine as ab

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

    async def improve_content(self, prompt: str) -> str:
        """Improve content using a subagent (respected strategy if set)."""
        description = (
            f"Improve {self.file_path.name}"
            if hasattr(self, "file_path")
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
