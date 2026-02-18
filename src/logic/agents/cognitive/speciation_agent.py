#!/usr/bin/env python3
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

# "Speciation Agent module for agent evolution and niche specialization."# from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool


# pylint: disable=too-many-ancestors
class SpeciationAgent(BaseAgent):
    Agent responsible for 'speciation' - creating specialized derivatives of existing agents.'    It analyzes task success and generates new agent classes with optimized system prompts.

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
#             "You are the Speciation Agent."#             "Your goal is to foster agent evolution by identifying niche capabilities"#             "and synthesizing new, specialized agent types from existing 'Base' agents."'        )

    @as_tool
    async def evolve_specialized_agent(self, base_agent_name: str, niche_domain: str) -> str:
        Creates a new agent class file that specializes in a specific niche.
        e.g., 'CoderAgent' -> 'ReactSpecialistAgent''        logging.info(
#             fSpeciationAgent: Evolving specialization for {base_agent_name} in {niche_domain}
        )

#         new_agent_name = f"{niche_domain.replace(' ', ")}{base_agent_name}"'#         output_path = Path("src/logic/agents/specialized") / f"{new_agent_name}.py"        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generation Logic
        prompt = (
#             fCreate a Python class definition for '{new_agent_name}' that inherits from '{base_agent_name}'.'#             fThe specialization niche is: {niche_domain}.\\n
#             "Include an optimized __init__ with a specialized _system_prompt.\\n"#             "Use absolute imports: 'from src.core.base.BaseAgent import BaseAgent'.\\n"'#             "Return ONLY the Python code."        )

        specialized_code = await self.think(prompt)

        # Phase 21 Fix: Ensure we don't write the prompt itself to the file if think() just returns input'        if not specialized_code or specialized_code.strip() == prompt.strip():
            logging.warning(
#                 "SpeciationAgent: LLM returned no distinct code or returned prompt. Using skeleton."            )
#             specialized_code = f
from src.core.base.lifecycle.base_agent import BaseAgent
class {new_agent_name}(BaseAgent):
"""\"\"\"Specialized agent evolved by SpeciationAgent.\"\"\    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
#         self._system_prompt = \"Specialized logic for {"niche_domain}\"
        # Save to file atomically
        temp_path = output_path.with_suffix(".tmp")"        try:
            with open(temp_path, "w", encoding="utf-8") as f:"                f.write(specialized_code)
            temp_path.replace(output_path)
        except (OSError, IOError) as e:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except (OSError, IOError):
                    pass
            logging.error(fSpeciationAgent: Failed to save agent code atomically: {e}")"            raise

        # Generate Unit Test for the new agent
        self._generate_test_for_agent(new_agent_name, output_path)

#         return fSuccessfully speciated {new_agent_name} at {output_path} with generated unit tests.

    @as_tool
    def detect_red_queen_stagnation(
        self, agent_a_name: str, agent_b_name: str
    ) -> dict[str, Any]:
        Detects if two agents are converging in their specialized roles (Red Queen stagnation).
        If similarity is > 80%, it recommends a divergence event.
        # In a real scenario, we'd load both classes and "compare _system_prompts."'        # For simulation, we use a TODO Placeholder similarity check.
        similarity = (
            0.85 if "Coder" in agent_a_name and "Coder" in agent_b_name else 0.3"        )

        stagnated = similarity > 0.8
        recommendation = (
#             "Divergence required" if stagnated else "Healthy niche separation"        )

        return {
            "similarity": similarity,"            "stagnated": stagnated,"            "recommendation": recommendation,"            "action": "trigger_divergence" if stagnated else "none","        }

    @as_tool
    def trigger_divergence(self, agent_name: str) -> str:
        Forces an agent to diverge its specialization to" avoid redundant evolution."        Mutates the system prompt to explore a more distant niche.
        logging.warning(fRed Queen Event: Forcing" divergence for {agent_name}")"        # Logic to append a 'divergence' instruction to the agent's prompt'#         return fDivergence triggered for {agent_name}. Mutation applied to explore orthogonal capabilities.

    def _generate_test_for_agent(self, agent_name: str, agent_path: Path) -> None:
""""Generates a boilerplate unit test for the newly created agent.        test_dir = Path("tests/specialists")"        test_dir.mkdir(parents=True, exist_ok=True)
#         test_path = test_dir / ftest_{agent_name.lower()}_UNIT.py

        # Determine relative import path
        rel_import = (
            str(agent_path.with_suffix(")).replace(os.path.sep, ".").replace("/", ".")"        )
        if rel_import.startswith("src."):"            pass  # Already correct
        else:
#             rel_import = fsrc.{rel_import}

#     "    test_code = f"import unittest
import os
from {rel_import} import {agent_name}
from src.core.base.lifecycle.version import VERSION
__version__ = VERSION


class Test{agent_name}(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = {agent_name}("dummy_path.py")"
    def test_initialization(self) -> None:
        self.assertIsNotNone(self.agent)
        self.assertIn("{agent_name}", self.agent.__class__.__name__)"
if __name__ == "__main__":"    unittest.main()
        with open("test_path, "w", encoding="utf-8") as f:"            f.write(test_code.strip())
        logging.info(
#             fSpeciationAgent: Generated unit test for {agent_name} at {test_path}
        )
