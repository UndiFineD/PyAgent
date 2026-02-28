# Splice: src/infrastructure/engine/sampling/ngram/index.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- SuffixIndex
- SuffixTreeProposer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
