# Splice: src/infrastructure/engine/loading/expert_load_balancer.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ExpertType
- EplbMetrics
- ExpertMapping
- AbstractEplbPolicy
- DefaultEplbPolicy
- LocalityAwarePolicy
- ExpertLoadBalancer
- AsyncExpertRebalancer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
