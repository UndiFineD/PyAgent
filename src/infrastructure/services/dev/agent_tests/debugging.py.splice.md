# Splice: src/infrastructure/services/dev/agent_tests/debugging.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ExecutionReplayer
- TestProfiler
- TestRecorder
- TestReplayer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
