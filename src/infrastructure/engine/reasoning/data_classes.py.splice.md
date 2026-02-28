# Splice: src/infrastructure/engine/reasoning/data_classes.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ReasoningToken
- ThinkingBlock
- ToolCall
- ToolCallResult
- ParseResult

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
