# Splice: src/infrastructure/services/dev/scripts/analysis/run_fleet_self_improvement.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- DirectiveParser
- IntelligenceHarvester
- CycleOrchestrator

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
