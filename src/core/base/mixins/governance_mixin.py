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

"""Governance Mixin for BaseAgent."""

import asyncio
import logging
from typing import Any

from src.core.base.logic.managers.resource_quota_manager import (
    QuotaConfig, ResourceQuotaManager)


class GovernanceMixin:
    """Handles resource quotas, preemption, and security clearance."""

    def __init__(self, config: Any, **_kwargs: Any) -> None:
        self.quotas = ResourceQuotaManager(
            config=QuotaConfig(
                max_tokens=getattr(config, "max_tokens_per_session", None),
                max_time_seconds=getattr(config, "max_time_per_session", None),
            )
        )
        self._suspended: bool = False

    async def check_preemption(self) -> None:
        """Wait if the agent is suspended."""
        while self._suspended:
            await asyncio.sleep(0.5)

    def suspend(self) -> None:
        """Suspend agent execution."""
        self._suspended = True

    def resume(self) -> None:
        """Resume agent execution."""
        self._suspended = False

    async def request_firewall_clearance(self, thought: str) -> bool:
        """Inform fleet of thought and wait for FirewallAgent clearance."""
        # Check for clearance (avoid recursion for FirewallAgent)
        if self.__class__.__name__ == "FirewallAgent":
            return True

        registry: Any | None = getattr(self, "registry", None)
        if not registry and hasattr(self, "fleet") and self.fleet:
            registry: Any | None = getattr(self.fleet, "signals", None)

        if registry:
            try:
                await registry.emit(
                    "thought_stream",
                    {"agent": self.__class__.__name__, "thought": thought},
                )
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logging.debug("Thought emission failed: %s", e)

        try:
            # pylint: disable=import-outside-toplevel
            from src.logic.agents.security.firewall_agent import FirewallAgent

            firewall = None
            if hasattr(self, "fleet") and self.fleet:
                firewall = self.fleet.agents.get("FirewallAgent")

            if not firewall:
                firewall = FirewallAgent()

            return await firewall.request_clearance_blocking(self.__class__.__name__, thought)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.debug("Firewall clearance defaulted to True (Error: %s)", e)
            return True
