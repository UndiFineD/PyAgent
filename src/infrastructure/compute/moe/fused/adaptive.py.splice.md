# Splice: src/infrastructure/compute/moe/fused/adaptive.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- AdaptiveMoELayer
- HierarchicalMoELayer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
