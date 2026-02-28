# Splice: src/observability/stats/agents.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- StatsAgent
- ReportingAgent
- TransparencyAgent

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
