# Splice: src/infrastructure/engine/structured/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- FSMState
- FSMTransitionTable
- TokenMask

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
