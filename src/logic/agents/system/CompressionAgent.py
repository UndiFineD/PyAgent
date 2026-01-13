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

"""CompressionAgent for PyAgent.
Specializes in context window optimization, recursive summarization, 
and minimizing token usage for long-running sub-swarm dialogues.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import Dict, List
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

__version__ = VERSION

class CompressionAgent(BaseAgent):
    """Agent that compresses multi-turn histories into essential state representations."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Compression Agent. Your goal is to maximize information density. "
            "You summarize internal dialogues, extract core decision points, and remove redundant chatter. "
            "Deliver a high-fidelity summary that fits within a small token budget."
        )

    @as_tool
    def compress_history(self, history: list[dict[str, str]], target_tokens: int = 500) -> str:
        """Compresses a conversation history into a dense summary block."""
        logging.info(f"CompressionAgent: Summarizing {len(history)} messages into ~{target_tokens} tokens.")
        
        # Serialize history for prompting
        history_text = "\n".join([f"{m.get('role', 'user')}: {m.get('content', '')}" for m in history])
        
        prompt = (
            f"Please compress the following conversation history into a dense summary. "
            f"Focus on key decisions, tool outputs, and unresolved state. "
            f"Target length: {target_tokens} vocabulary-rich tokens.\n\n"
            f"HISTORY:\n{history_text}"
        )
        
        compressed_summary = self.think(prompt)
        return compressed_summary

    @as_tool
    def extract_gist(self, complex_report: str) -> str:
        """Extracts the 'gist' or 'bottom line' from a technical report."""
        logging.info("CompressionAgent: Extracting gist from report.")
        prompt = f"Provide a one-paragraph 'gist' of this technical report. Focus on the final conclusion.\n\nREPORT:\n{complex_report}"
        return self.think(prompt)

    def improve_content(self, prompt: str) -> str:
        return "Context compression logic is active. Information density is optimal."

if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(CompressionAgent, "Compression Agent", "Token efficiency and summarization optimizer")
    main()