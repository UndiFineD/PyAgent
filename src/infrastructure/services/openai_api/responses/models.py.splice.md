# Splice: src/infrastructure/services/openai_api/responses/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ContentPart
- TextContent
- ImageContent
- AudioContent
- RefusalContent
- ToolCallContent
- Message
- ToolDefinition
- ResponseConfig
- ResponseUsage
- ResponseOutput
- Response

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
