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

"""Agent specializing in automated paper-to-tool generation.
Ingests SOTA research (simulated) and generates new agentic tools.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from .ResearchCore import ResearchCore

__version__ = VERSION




class ResearchAgent(BaseAgent):
    """Analyzes research papers and drafts new tool implementations using the SGI-Bench DCAP Cycle."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.core = ResearchCore()
        self._system_prompt = (
            "You are the SOTA Research Agent. "
            "You follow the SGI-Bench (Scientific General Intelligence) DCAP cycle:\n"
            "1. Deliberation: Deeply understand the research problem.\n"
            "2. Conception: Formulate a hypothesis or algorithmic model.\n"
            "3. Action: Implement the model into code/tools.\n"
            "4. Perception: Validate the implementation against constraints.\n"
            "Always cite the source and ensure type safety."
        )

    @as_tool
    def dcap_research(self, topic: str, content: str) -> dict[str, str]:
        """Executes a full Deliberation-Conception-Action-Perception cycle on a topic."""
        logging.info(f"RESEARCH: Executing DCAP cycle for {topic}")

        result = self.core.execute_dcap_cycle(topic, content)

        if self.memory and hasattr(self.memory, 'add_entity'):
            self.memory.add_entity(topic, {"type": "dcap_research", "data": result})

        return result

    @as_tool
    def ingest_paper(self, title: str, summary: str) -> str:
        """Analyzes a research paper summary and identifies new capabilities."""










        logging.info(f"RESEARCH: Ingesting paper '{title}'")
        analysis = self.core.analyze_paper(title, summary)

        if self.memory and hasattr(self.memory, 'add_entity'):




            self.memory.add_entity(title, {"type": "paper", "summary": summary, "analysis": analysis})

        return f"Successfully ingested paper '{title}'. Capabilities identified for tool generation."

    @as_tool


    def generate_tool_from_research(self, title: str) -> str:
        """Drafts a Python tool implementation based on an ingested paper."""
        logging.info(f"RESEARCH: Generating tool based on {title}")
        tool_code = self.core.draft_tool_code(title)
        return tool_code



        return f"Tool draft generated for '{title}':\n{tool_code}"

    def improve_content(self, prompt: str) -> str:
        return f"ResearchAgent scanning for SOTA updates: {prompt}"





if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(ResearchAgent, "Research Agent", "Research database path")
    main()
