# Splice: src/infrastructure/services/tools/parser/base.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ToolParserType
- ToolCallStatus
- ToolParameter
- ToolCall
- ToolParseResult
- StreamingToolState
- ToolParser

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
