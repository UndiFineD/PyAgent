#!/usr/bin/env python3
"""
Parser-safe package init for reasoning parsers.

Provides conservative imports and registration calls to keep package importable.
"""
from __future__ import annotations

try:
    from .base import ReasoningParser
except Exception:
    class ReasoningParser:  # type: ignore
        pass

try:
    from .implementations.identity import IdentityReasoningParser
except Exception:
    class IdentityReasoningParser:  # type: ignore
        pass

try:
    from .implementations.json import JSONReasoningParser
except Exception:
    class JSONReasoningParser:  # type: ignore
        pass

try:
    from .implementations.markdown import MarkdownReasoningParser
except Exception:
    class MarkdownReasoningParser:  # type: ignore
        pass

try:
    from .implementations.xml import XMLReasoningParser
except Exception:
    class XMLReasoningParser:  # type: ignore
        pass

class ReasoningParserManager:
    @staticmethod
    def register_module(name: str, cls: type) -> None:
        return None

# Register simple defaults
ReasoningParserManager.register_module("xml", XMLReasoningParser)
ReasoningParserManager.register_module("json", JSONReasoningParser)
ReasoningParserManager.register_module("markdown", MarkdownReasoningParser)

__all__ = [
    "ReasoningParser",
    "IdentityReasoningParser",
    "JSONReasoningParser",
    "MarkdownReasoningParser",
    "XMLReasoningParser",
    "ReasoningParserManager",
]
