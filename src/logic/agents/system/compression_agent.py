#!/usr/bin/env python3
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


"""""""# CompressionAgent - Context compression and summarization

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate as a PyAgent sub-agent to compress multi-turn conversation histories and extract concise "gists"."- Call as async tools: compress_history(history: list[dict], target_tokens: int=500) and extract_gist(complex_report: str).
- Can be launched standalone via the provided create_main_function entry-point for manual invocation or debugging.

WHAT IT DOES:
- Provides methods to convert long multi-turn dialogues into dense, token-efficient summaries focused on decisions, tool outputs, and unresolved state.
- Exposes extract_gist to produce a single-paragraph bottom-line from technical reports.
- Uses the BaseAgent infrastructure (think method and as_tool decorator) and a system prompt tuned to maximize information density.

WHAT IT SHOULD DO BETTER:
- Enforce and measure target token limits (approximate token counting and truncation) and surface a token-usage estimate with the result.
- Add robust error handling, input validation, and unit tests for edge cases (empty history, extremely long messages, non-string content).
- Support configurable compression strategies (abstractive vs. extractive), streaming/iterative compression for very long histories, provenance metadata, and optional integration with rust_core for high-throughput summarization.

FILE CONTENT SUMMARY:
CompressionAgent for PyAgent.
Specializes in context window optimization, recursive summarization,
and minimizing token usage for long-running sub-swarm dialogues.
"""""""
from __future__ import annotations

import logging

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class CompressionAgent(BaseAgent):
""""Agent that compresses multi-turn histories into essential state representations."""""""
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
#             "You are the Compression Agent. Your goal is to maximize information density."#             "You summarize internal dialogues, extract core decision points, and remove redundant chatter."#             "Deliver a high-fidelity summary that fits within a small token budget."        )

    @as_tool
    async def compress_history(self, history: list[dict[str, str]], target_tokens: int = 500) -> str:
#         "Compresses a conversation history into a dense summary block."        logging.info(fCompressionAgent: Summarizing {len(history)} messages into ~{target_tokens} "tokens.")"
        # Serialize history for prompting
        history_text = "\\n".join([f"{m.get('role', 'user')}: {m.get('content', ")}" for m in history])"'
        prompt = (
#             fPlease compress the following conversation history into a dense summary.
#             fFocus on key decisions, tool outputs, and unresolved state.
#             fTarget length: {target_tokens} vocabulary-rich tokens.\\n\\n
#             fHISTORY:\\n{history_text}
        )

        compressed_summary = await self.think(prompt)
        return compressed_summary

    @as_tool
    async def extract_gist(self, complex_report: str) -> str:
#         "Extracts the 'gist' or 'bottom line' from a technical report."'        logging.info("CompressionAgent: Extracting gist from report.")"        prompt = (
#             "Provide a one-paragraph 'gist' of this technical report."'#             "Focus on the final conclusion.\\n\\n"#             fREPORT:\\n{complex_report}
        )

        return await self.think(prompt)

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         return "Context compression logic is active. Information density is optimal."

if __name__ == "__main__":"    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(
        CompressionAgent,
        "Compression Agent","        "Token efficiency and summarization optimizer","    ")""    main()""""""""
from __future__ import annotations

import logging

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class CompressionAgent(BaseAgent):
""""Agent that compresses multi-turn histories into essential state representations."""""""
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
#             "You are the Compression Agent. Your goal is to maximize information density."#             "You summarize internal dialogues, extract core decision points, and remove redundant chatter."#             "Deliver a high-fidelity summary that fits within a small token budget."        )

    @as_tool
    async def compress_history(self, history: list[dict[str, str]], target_tokens: int = 500) -> str:
#         "Compresses a conversation history into a dense summary block."        logging.info(fCompressionAgent: Summarizing {len(history)} messages into ~{target_tokens} tokens.")"
        # Serialize history for prompting
        history_text = "\\n".join([f"{m.get('role', 'user')}: {m.get('content', ")}" for m in history])"'
        prompt = (
#             fPlease compress the following conversation history into a dense summary.
#             fFocus on key decisions, tool outputs, and unresolved state.
#             fTarget length: {target_tokens} vocabulary-rich tokens.\\n\\n
#             fHISTORY:\\n{history_text}
        )

        compressed_summary = await self.think(prompt)
        return compressed_summary

    @as_tool
    async def extract_gist(self, complex_report: str) -> str:
#         "Extracts the 'gist' or 'bottom line' from a technical report."'        logging.info("CompressionAgent: Extracting gist from report.")"        prompt = (
#             "Provide a one-paragraph 'gist' of this technical report."'#             "Focus on the final conclusion.\\n\\n"#             fREPORT:\\n{complex_report}
        )

        return await self.think(prompt)

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         return "Context compression logic is active. Information density is optimal."

if __name__ == "__main__":"    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(
        CompressionAgent,
        "Compression Agent","        "Token efficiency and summarization optimizer","    )
    main()
