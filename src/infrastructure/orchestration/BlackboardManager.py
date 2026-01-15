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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Shared central memory for opportunistic agent collaboration (Blackboard Pattern)."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import Any
from .BlackboardCore import BlackboardCore

__version__ = VERSION




class BlackboardManager:
    """
    Central repository for agents to post findings and look for data.
    Shell for BlackboardCore.
    """

    def __init__(self) -> None:
        self.core = BlackboardCore()

    def post(self, key: str, value: Any, agent_name: str) -> None:
        """Post data to the blackboard."""
        logging.info(f"Blackboard: Agent {agent_name} posted to {key}")
        self.core.process_post(key, value, agent_name)

    def get(self, key: str) -> Any:
        """Retrieve data from the blackboard."""
        return self.core.get_value(key)

    def list_keys(self) -> list[str]:
        """List all available keys on the blackboard."""
        return self.core.get_all_keys()
