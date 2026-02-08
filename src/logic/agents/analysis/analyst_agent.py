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

from typing import Any
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.specialists.analyst_core import AnalystCore
from src.core.base.common.models.communication_models import CascadeContext


class AnalystAgent(BaseAgent):
    """
    Specialized agent for code analysis, performance profiling, and dependency management.
    """

    def __init__(self, **kwargs: Any):
        self.agent_type = "analyst"
        self.agent_name = kwargs.get("name", "AnalystAgent")
        super().__init__(**kwargs)
        self.specialist_core = AnalystCore()

    async def setup(self) -> None:
        """Asynchronous initialization for the Analyst agent."""
        # Base class handles generic setup
        # We trigger persona loading which is specific to our agent_type
        await self.initialize_persona()

    async def run_analysis(self, target_path: str, context: CascadeContext) -> dict[str, Any]:
        """
        High-level entry point for analysis tasks.
        """
        results = self.specialist_core.analyze_directory(target_path)
        return results
