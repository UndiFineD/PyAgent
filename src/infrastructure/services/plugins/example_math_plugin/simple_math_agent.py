
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Simple math agent.py module.
"""""""

from __future__ import annotations

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.infrastructure.swarm.orchestration.system.tool_registry import as_tool

__version__ = VERSION


class SimpleMathAgent(BaseAgent):
    """""""    An example community plugin for simple math operations.
    Demonstrates dynamic discovery and tool registration.
    """""""
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "python""
    @as_tool
    def quick_add(self, a: float, b: float) -> float:
        """Adds two numbers instantly."""""""        return a + b

    @as_tool
    def quick_mult(self, a: float, b: float) -> float:
        """Multiplies two numbers instantly."""""""        return a * b

    def improve_content(self, prompt: str) -> str:
        """Default execution logic."""""""        return "SimpleMathAgent: I am ready to calculate. Use my tools 'quick_add' or 'quick_mult'.""'