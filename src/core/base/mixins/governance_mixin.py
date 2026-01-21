#!/usr/bin/env python3
# Governance Mixin for BaseAgent
import asyncio
import logging
from typing import Any
from src.core.base.logic.managers.resource_quota_manager import ResourceQuotaManager, QuotaConfig

class GovernanceMixin:
    """Handles resource quotas, preemption, and security clearance."""

    def __init__(self, config: Any, **kwargs: Any) -> None:
        self.quotas = ResourceQuotaManager(
            config=QuotaConfig(
                max_tokens=getattr(config, "max_tokens_per_session", None),
                max_time_seconds=getattr(config, "max_time_per_session", None),
            )
        )
        self._suspended: bool = False

    async def _check_preemption(self) -> None:
        while self._suspended:
            await asyncio.sleep(0.5)

    def suspend(self) -> None:
        self._suspended = True

    def resume(self) -> None:
        self._suspended = False

    async def _request_firewall_clearance(self, thought: str) -> bool:
        """Inform fleet of thought and wait for FirewallAgent clearance."""
        # Check for clearance (avoid recursion for FirewallAgent)
        if self.__class__.__name__ == "FirewallAgent":
            return True

        registry = getattr(self, "registry", None)
        if not registry and hasattr(self, "fleet") and self.fleet:
            registry = getattr(self.fleet, "signals", None)

        if registry:
            try:
                await registry.emit(
                    "thought_stream",
                    {"agent": self.__class__.__name__, "thought": thought},
                )
            except Exception as e:
                logging.debug(f"Thought emission failed: {e}")

        try:
            from src.logic.agents.security.firewall_agent import FirewallAgent
            firewall = None
            if hasattr(self, "fleet") and self.fleet:
                firewall = self.fleet.agents.get("FirewallAgent")

            if not firewall:
                firewall = FirewallAgent()

            return await firewall.request_clearance_blocking(
                self.__class__.__name__, thought
            )
        except Exception as e:
            logging.debug(f"Firewall clearance defaulted to True (Error: {e})")
            return True
