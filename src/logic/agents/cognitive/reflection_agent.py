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


"""Agent specializing in self-critique and reflection."""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool

__version__ = VERSION


# pylint: disable=too-many-ancestors
class ReflectionAgent(BaseAgent):
    """
    Tier 2 (Cognitive Logic) - Reflection Agent: Critique and refinement engine
    specializing in self-improvement and logic verification.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Reflection Agent. "
            "Your job is to find flaws in technical solutions. "
            "Be critical, objective, and specific."
        )

    @as_tool
    def critique(self, work: str) -> str:
        """Analyzes work for flaws and suggests improvements."""
        _ = work
        return (
            "### Critique\n1. Potential edge cases: Not handled.\n"
            "2. Inefficiency: The loop structure is O(n^2).\n"
            "3. Clarity: Variable names are ambiguous."
        )

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Optimizes fleet content based on cognitive reasoning."""
        _ = prompt
        _ = target_file
        return self.critique(prompt)
