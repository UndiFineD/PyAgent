# Splice: src/core/base/logic/managers/system_managers.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- EventManager
- StatePersistence
- FilePriorityManager
- HealthChecker
- ProfileManager
- ResponseCache

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
