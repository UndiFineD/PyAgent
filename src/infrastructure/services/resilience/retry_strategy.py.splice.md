# Splice: src/infrastructure/services/resilience/retry_strategy.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- JitterType
- RetryStats
- RetryExhaustedError
- RetryStrategy
- RetryBudget

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
