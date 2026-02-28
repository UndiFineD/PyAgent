# Splice: src/infrastructure/engine/speculative/ngram_proposer.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- NgramConfig
- NgramMatch
- NgramProposalResult
- NgramCache
- NgramProposer
- WeightedNgramProposer
- PromptLookupProposer
- HybridNgramProposer
- NgramProposerFactory

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
