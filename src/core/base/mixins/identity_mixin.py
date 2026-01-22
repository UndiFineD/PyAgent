#!/usr/bin/env python3
# Identity Mixin for BaseAgent
from typing import Any
from src.core.base.common.models import AgentPriority
from src.core.base.logic.core.identity_core import IdentityCore


class IdentityMixin:
    """Handles agent identity, configuration, and capabilities."""

    def __init__(self, **kwargs: Any) -> None:
        self.identity = IdentityCore(
            agent_type=self.__class__.__name__.lower().replace("agent", "") or "base"
        )
        self.agent_name = self.identity.agent_type
        self.capabilities: list[str] = ["base"]
        self.priority: AgentPriority = kwargs.get("priority", AgentPriority.NORMAL)
        self._suspended: bool = False

    def get_capabilities(self) -> list[str]:
        return self.capabilities

    def _register_capabilities(self) -> None:
        """Emits a signal with agent capabilities for discovery."""
        try:
            import asyncio
            from src.infrastructure.swarm.orchestration.signals.signal_registry import SignalRegistry

            signals = SignalRegistry()
            # Note: We expect the class using this mixin to have agent_logic_core
            if hasattr(self, "agent_logic_core"):
                payload = self.agent_logic_core.prepare_capability_payload(
                    self.__class__.__name__, self.get_capabilities()
                )

                try:
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)

                    if loop.is_running():
                        asyncio.create_task(
                            signals.emit("agent_capability_registration", payload)
                        )
                    else:
                        loop.run_until_complete(
                            signals.emit("agent_capability_registration", payload)
                        )
                except Exception:
                    pass
        except Exception:
            pass
