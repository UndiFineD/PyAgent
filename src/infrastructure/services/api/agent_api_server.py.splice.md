# Splice: src/infrastructure/services/api/agent_api_server.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- TaskRequest
- TelemetryManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
