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

from __future__ import annotations
from datetime import datetime
from typing import Any
from src.core.base.BaseModules import BaseModule


class SignalModule(BaseModule):
    """
    Consolidated core module for signal processing.
    Migrated from SignalCore.
    """

    def initialize(self) -> bool:
        """Initialize signal handlers."""
        return super().initialize()

    def execute(self, action: str, **kwargs) -> Any:
        """
        Executes signal-related logic.
        Supported actions: create_event, prune_history
        """
        if not self.initialized:
            self.initialize()

        if action == "create_event":
            return self.create_event(
                kwargs.get("signal_name", "generic"),
                kwargs.get("data"),
                kwargs.get("sender", "unknown"),
            )
        elif action == "prune_history":
            return self.prune_history(
                kwargs.get("history", []), kwargs.get("limit", 100)
            )
        return None

    def create_event(self, signal_name: str, data: Any, sender: str) -> dict[str, Any]:
        """Creates a standardized signal event object."""
        return {
            "signal": signal_name,
            "data": data,
            "sender": sender,
            "timestamp": datetime.now().isoformat(),
        }

    def prune_history(
        self, history: list[dict[str, Any]], limit: int
    ) -> list[dict[str, Any]]:
        """Returns the last N events from the signal history."""
        return history[-limit:]

    def shutdown(self) -> bool:
        """Cleanup signal module."""
        return super().shutdown()
