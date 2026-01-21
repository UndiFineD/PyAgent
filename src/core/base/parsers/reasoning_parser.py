# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
ReasoningParser - Extensible framework for extracting reasoning from LLM outputs.
(Facade for modular implementation)
"""

from .reasoning import (
    ReasoningResult,
    StreamingReasoningState,
    ReasoningParser,
    ReasoningParserManager,
    reasoning_parser,
    extract_reasoning,
    create_streaming_parser,
    XMLReasoningParser,
    JSONReasoningParser,
    MarkdownReasoningParser,
    IdentityReasoningParser,
)

__all__ = [
    "ReasoningResult",
    "StreamingReasoningState",
    "ReasoningParser",
    "ReasoningParserManager",
    "reasoning_parser",
    "extract_reasoning",
    "create_streaming_parser",
    "XMLReasoningParser",
    "JSONReasoningParser",
    "MarkdownReasoningParser",
    "IdentityReasoningParser",
]
