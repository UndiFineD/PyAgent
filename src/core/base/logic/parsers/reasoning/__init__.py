# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from src.core.base.common.models import ReasoningResult, StreamingReasoningState
from .base import ReasoningParser
from .registry import ReasoningParserManager, reasoning_parser
from src.core.base.common.utils import extract_reasoning, create_streaming_parser
from .implementations.xml import XMLReasoningParser
from .implementations.json import JSONReasoningParser
from .implementations.markdown import MarkdownReasoningParser
from .implementations.identity import IdentityReasoningParser

# Register built-in parsers
ReasoningParserManager.register_module("xml", XMLReasoningParser)
ReasoningParserManager.register_module("json", JSONReasoningParser)
ReasoningParserManager.register_module("markdown", MarkdownReasoningParser)
ReasoningParserManager.register_module("identity", IdentityReasoningParser)

# Aliases
ReasoningParserManager.register_module("think", XMLReasoningParser)
ReasoningParserManager.register_module("none", IdentityReasoningParser)

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
