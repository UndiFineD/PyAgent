# Splice: src/infrastructure/engine/sampling/beam_search.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- BeamSearchConfig
- BeamHypothesis
- BeamSearchSampler

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
