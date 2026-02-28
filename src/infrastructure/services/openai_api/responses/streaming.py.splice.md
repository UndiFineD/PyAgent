# Splice: src/infrastructure/services/openai_api/responses/streaming.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- SSEEvent
- SSEStream
- StreamingHandler

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
