# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from dataclasses import dataclass, field

@dataclass
class ReasoningResult:
    """
    Result of reasoning extraction.

    Attributes:
        reasoning: The extracted reasoning/thinking content.
        content: The extracted content/answer.
        reasoning_tokens: Token IDs for reasoning (if available).
        content_tokens: Token IDs for content (if available).
        is_complete: Whether reasoning extraction is complete.
    """
    reasoning: str | None = None
    content: str | None = None
    reasoning_tokens: list[int] | None = None
    content_tokens: list[int] | None = None
    is_complete: bool = True


@dataclass
class StreamingReasoningState:
    """
    State for streaming reasoning extraction.

    Tracks the current state of reasoning extraction during streaming.
    """
    accumulated_text: str = ""
    accumulated_tokens: list[int] = field(default_factory=list)
    in_reasoning: bool = False
    reasoning_buffer: str = ""
    content_buffer: str = ""
    reasoning_complete: bool = False
