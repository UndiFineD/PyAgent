# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from typing import Any
from .registry import ReasoningParserManager
from src.core.base.common.models import ReasoningResult, StreamingReasoningState


def extract_reasoning(
    model_output: str,
    parser_name: str = "xml",
    tokenizer: Any = None,
    **kwargs: Any,
) -> ReasoningResult:
    """
    Convenience function to extract reasoning from model output.
    """
    parser = ReasoningParserManager.create_parser(parser_name, tokenizer, **kwargs)
    return parser.extract_reasoning(model_output)


def create_streaming_parser(
    parser_name: str = "xml",
    tokenizer: Any = None,
    **kwargs: Any,
) -> tuple[Any, StreamingReasoningState]:
    """
    Create a parser and state for streaming extraction.
    """
    parser = ReasoningParserManager.create_parser(parser_name, tokenizer, **kwargs)
    state = StreamingReasoningState()
    return parser, state
