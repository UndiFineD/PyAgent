# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import re
import json
from typing import Any, ClassVar, Sequence
from ..base import ReasoningParser
from ..models import ReasoningResult, StreamingReasoningState


class JSONReasoningParser(ReasoningParser):
    """
    Parser for JSON-structured reasoning outputs.

    Expects output in format:
    {"reasoning": "...", "answer": "..."}
    """

    name: ClassVar[str] = "json"

    def __init__(
        self,
        tokenizer: Any = None,
        *,
        reasoning_key: str = "reasoning",
        answer_key: str = "answer",
        **kwargs: Any,
    ) -> None:
        super().__init__(tokenizer, **kwargs)
        self.reasoning_key = reasoning_key
        self.answer_key = answer_key

    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        if self.model_tokenizer is None:
            return False
        text = self.model_tokenizer.decode(input_ids)
        # Check for complete JSON
        try:
            data = json.loads(text)
            return self.answer_key in data
        except json.JSONDecodeError:
            return False

    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        if self.model_tokenizer is None:
            return input_ids

        text = self.model_tokenizer.decode(input_ids)
        result = self.extract_reasoning(text)
        if result.content:
            return self.model_tokenizer.encode(result.content, add_special_tokens=False)
        return input_ids

    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        try:
            data = json.loads(model_output)
            return ReasoningResult(
                reasoning=data.get(self.reasoning_key),
                content=data.get(self.answer_key),
            )
        except json.JSONDecodeError:
            # Try to extract JSON from text
            match = re.search(r'\{[^{}]*\}', model_output, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group())
                    return ReasoningResult(
                        reasoning=data.get(self.reasoning_key),
                        content=data.get(self.answer_key),
                    )
                except json.JSONDecodeError:
                    pass

            return ReasoningResult(content=model_output)

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

        # Try to parse as JSON
        result = self.extract_reasoning(current_text)
        if result.reasoning or result.content:
            state.reasoning_buffer = result.reasoning or ""
            state.content_buffer = result.content or ""
            state.reasoning_complete = True

        return result, state
