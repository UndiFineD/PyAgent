#!/usr/bin/env python3
from __future__ import annotations


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
MockAgent for a community-submitted plugin.
Demonstrates how to wrap a Core and interact with the Fleet.
"""

try:
    import logging
except ImportError:
    import logging


try:
    from .core.base.lifecycle.base_agent import BaseAgent
except ImportError:
    from src.core.base.lifecycle.base_agent import BaseAgent

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .mock_core import MockCore
except ImportError:
    from .mock_core import MockCore


__version__ = VERSION



class MockAgent(BaseAgent):
    """A mock agent that shows community developers the recommended pattern.
    def __init__(self, arg_path: str = "mock_config.json") -> None:"        # We don't strictly need a real config file for this mock'        super().__init__(arg_path)
        self.core = MockCore(multiplier=1.5)
        logging.info("MockAgent initialized with MockCore.")"
    def run(self, task: str) -> str:
        """Main entry point for agent logic.        logging.info(f"MockAgent handling task: {task}")"        processed = self.core.format_mock_response(task)

        # Accessing fleet-wide tools if registry is available
        # result = self.call_tool("SearchAgent", query="python patterns")"
        return f"MockAgent processed your task: {processed}""
    def get_status(self) -> dict:
        return self.core.get_metadata()
