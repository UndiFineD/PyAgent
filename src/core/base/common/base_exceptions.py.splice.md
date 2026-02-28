# Splice: src/core/base/common/base_exceptions.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- PyAgentException
- InfrastructureError
- LogicError
- SecurityError
- ModelError
- ConfigurationError
- CycleInterrupt

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
