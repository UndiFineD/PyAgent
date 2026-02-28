# Splice: src/infrastructure/engine/engine_lifecycle.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- EngineState
- EngineConfig
- EngineLifecycleManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
