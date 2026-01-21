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
from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool

__version__ = VERSION


class CognitiveSuperAgent(BaseAgent):
    """
    Cognitive Super-Agent: A fused agent combining Reasoning and Reflection
    capabilities for high-performance cognitive workflows.
    """

    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path

    @as_tool
    def accelerated_think(self, prompt: str) -> str:
        """Combines reasoning and reflection into a single step."""
        # Simulated fused logic
        reasoning = f"Reasoning about: {prompt}"
        reflection = f"Reflecting on reasoning: {reasoning}"
        return f"Final cognitive output: {reflection}"

    def improve_content(self, content: str) -> str:
        """Override to use cognitive acceleration."""
        return self.accelerated_think(content)
