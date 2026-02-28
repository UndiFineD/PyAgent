# Splice: src/infrastructure/engine/incremental_detokenizer.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- StopMatch
- IncrementalDetokenizer
- NoOpDetokenizer
- BaseIncrementalDetokenizer
- FastIncrementalDetokenizer
- SlowIncrementalDetokenizer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
