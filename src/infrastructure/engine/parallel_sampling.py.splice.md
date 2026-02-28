# Splice: src/infrastructure/engine/parallel_sampling.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- SamplingStrategy
- OutputKind
- SamplingParams
- CompletionOutput
- ParentRequest
- ParallelSamplingManager
- BeamState
- BeamSearchManager
- DiverseSamplingManager
- BestOfNFilter
- IterationStats

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
