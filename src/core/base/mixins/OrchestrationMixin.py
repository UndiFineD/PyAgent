#!/usr/bin/env python3
# Orchestration Mixin for BaseAgent
from typing import Any, Optional
import logging

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
