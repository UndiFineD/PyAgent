# Splice: src/core/base/common/base_interfaces.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- AgentInterface
- OrchestratorInterface
- CoreInterface
- ContextRecorderInterface
- Loadable
- Saveable
- Component

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
