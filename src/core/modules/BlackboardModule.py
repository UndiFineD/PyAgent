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
from typing import Any
from src.core.base.modules import BaseModule







class BlackboardModule(BaseModule):
    """
    Consolidated core module for Blackboard operations.
    Migrated from BlackboardCore.
    """
    def __init__(self, config:
        dict[str, Any] | None = None) -> None:
        super().__init__(config)
        self.data: dict[str, Any] = {}
        self.history: list[dict[str, Any]] = []

    def initialize(self) -> bool:
        """Initialize blackboard state."""
        return super().initialize()

    def execute(self, action:
        str, **kwargs) -> Any:
        """
        Executes blackboard operations.
        Supported actions: post, get, keys
        """
        if not self.initialized:
            self.initialize()

        if action == "post":
            return self.process_post(
                kwargs.get("key"),
                kwargs.get("value"),
                kwargs.get("agent_name", "unknown")
            )
        elif action == "get":
            return self.get_value(kwargs.get("key"))
        elif action == "keys":
            return self.get_all_keys()
        return None

    def process_post(self, key:
        str, value: Any, agent_name: str) -> dict[str, Any]:
        """Core logic for posting data."""
        self.data[key] = value
        entry = {"agent": agent_name, "key": key, "value": value}
        self.history.append(entry)
        return entry

    def get_value(self, key:
        str) -> Any:
        return self.data.get(key)

    def get_all_keys(self) -> list[str]:
        return list(self.data.keys())

    def shutdown(self) -> bool:
        """Cleanup blackboard."""
        return super().shutdown()
