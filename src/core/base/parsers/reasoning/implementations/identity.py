# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from typing import Any, ClassVar, Sequence
from ..base import ReasoningParser
from ..models import ReasoningResult, StreamingReasoningState


class IdentityReasoningParser(ReasoningParser):
    """
    No-op parser that returns the full output as content.
    """
    
    name: ClassVar[str] = "identity"
    
    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        return True
    
    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        return input_ids
    
    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
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
        state.content_buffer = current_text
        
        return ReasoningResult(content=delta_text), state
