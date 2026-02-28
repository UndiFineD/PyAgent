# Splice: src/infrastructure/services/resilience/circuit_breaker.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- CircuitState
- CircuitStats
- CircuitBreakerError
- CircuitBreaker
- CircuitBreakerRegistry

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
