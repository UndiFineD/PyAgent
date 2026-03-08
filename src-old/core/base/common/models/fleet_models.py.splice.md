# Splice: src/core/base/common/models/fleet_models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- HealthCheckResult
- IncrementalState
- RateLimitConfig
- TokenBudget
- ShutdownState

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
