#!/usr/bin/env python3
"""
Module: identity_mixin
Provides identity and metadata mixin for PyAgent agents.
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

"""Identity Mixin for BaseAgent."""

from asyncio import AbstractEventLoop
from asyncio import AbstractEventLoop
from typing import Any

from src.core.base.common.models import AgentPriority
from src.core.base.logic.core.identity_core import IdentityCore


class IdentityMixin:  # pylint: disable=too-few-public-methods
    """Handles agent identity, configuration, and capabilities."""

    def __init__(self, **kwargs: Any) -> None:
        self.identity = IdentityCore(agent_type=self.__class__.__name__.lower().replace("agent", "") or "base")
        self.agent_name: str = self.identity.agent_type
        self.capabilities: list[str] = ["base"]
        self.priority: AgentPriority = kwargs.get("priority", AgentPriority.NORMAL)
        self._suspended: bool = False
        # Phase 259: Context lineage tracking
        self.context: Any = None

    def get_capabilities(self) -> list[str]:
        """Return the agent capabilities."""
        return self.capabilities

    def _register_capabilities(self) -> None:
        """Emits a signal with agent capabilities for discovery."""
        try:
            # pylint: disable=import-outside-toplevel
            import asyncio

            from src.infrastructure.swarm.orchestration.signals.signal_registry import \
                SignalRegistry

            signals = SignalRegistry()
            # Note: We expect the class using this mixin to have agent_logic_core
            if hasattr(self, "agent_logic_core"):
                payload = getattr(self, "agent_logic_core").prepare_capability_payload(
                    self.__class__.__name__, self.get_capabilities()
                )

                try:
                    try:
                        loop: AbstractEventLoop = asyncio.get_running_loop()
                    except RuntimeError:
                        loop: AbstractEventLoop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)

                    if loop.is_running():
                        asyncio.create_task(signals.emit("agent_capability_registration", payload))
                    else:
                        loop.run_until_complete(signals.emit("agent_capability_registration", payload))
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    # pylint: disable=broad-exception-caught
                    pass
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            # pylint: disable=broad-exception-caught
            pass
