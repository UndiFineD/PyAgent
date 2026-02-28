# Splice: src/infrastructure/compute/moe/expert_router.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- RoutingMethod
- RouterConfig
- RouterOutput
- RouterBase
- TopKRouter
- GroupedTopKRouter
- ExpertChoiceRouter
- SoftMoERouter
- AdaptiveRouter
- RoutingSimulator

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
