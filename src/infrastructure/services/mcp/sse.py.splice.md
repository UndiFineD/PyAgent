# Splice: src/infrastructure/services/mcp/sse.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- SSEMCPServer
- MockSSEClient

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
