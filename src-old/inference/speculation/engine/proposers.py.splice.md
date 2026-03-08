# Splice: src/inference/speculation/engine/proposers.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- NgramProposer
- SuffixProposer
- EagleProposer
- HybridDrafter

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
