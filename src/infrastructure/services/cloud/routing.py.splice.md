# Splice: src/infrastructure/services/cloud/routing.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- RoutingStrategy
- ProviderMetrics
- RoutingConstraints
- IntelligentRouter

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
