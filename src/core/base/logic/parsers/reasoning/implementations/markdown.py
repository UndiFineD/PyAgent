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

"""
Markdown.py module.
"""

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import re
from typing import Any, ClassVar, Sequence

from ..base import ReasoningParser
from ..models import ReasoningResult, StreamingReasoningState


class MarkdownReasoningParser(ReasoningParser):
    """
    Parser for Markdown-style think blocks.

    Extracts reasoning from ```thinking blocks or > prefixed lines.
    """

    name: ClassVar[str] = "markdown"

    def __init__(
        self,
        tokenizer: Any = None,
        *,
        block_type: str = "thinking",
        **kwargs: Any,
    ) -> None:
        super().__init__(tokenizer, **kwargs)
        self.block_type = block_type
        self._pattern = re.compile(
            rf"```{re.escape(block_type)}\n(.*?)```",
            re.DOTALL,
        )

    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        if self.model_tokenizer is None:
            return False
        text = self.model_tokenizer.decode(input_ids)
        # Check for complete thinking block
        return bool(self._pattern.search(text))

    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        if self.model_tokenizer is None:
            return input_ids

        text = self.model_tokenizer.decode(input_ids)
        content = self._pattern.sub("", text).strip()
        return self.model_tokenizer.encode(content, add_special_tokens=False)

    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        matches = self._pattern.findall(model_output)
        reasoning = "\n".join(matches) if matches else None
        content = self._pattern.sub("", model_output).strip()

        return ReasoningResult(
            reasoning=reasoning,
            content=content if content else None,
        )

    def extract_reasoning_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
        state: StreamingReasoningState | None = None,
    ) -> tuple[ReasoningResult, StreamingReasoningState]:
        if state is None:
            state = StreamingReasoningState()

        state.accumulated_text = current_text
        result = self.extract_reasoning(current_text)

        if result.reasoning:
            state.reasoning_buffer = result.reasoning
            state.reasoning_complete = True
        if result.content:
            state.content_buffer = result.content

        return result, state
