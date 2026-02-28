# Splice: src/core/base/logic/parsers/tool_parser.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ToolCall
- ExtractedToolCalls
- StreamingToolCallDelta
- ToolParser
- JSONToolParser
- XMLToolParser
- ToolParserManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
