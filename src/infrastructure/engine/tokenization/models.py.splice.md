# Splice: src/infrastructure/engine/tokenization/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- TokenizerBackend
- SpecialTokenHandling
- TruncationStrategy
- PaddingStrategy
- TokenizerConfig
- TokenizerInfo
- TokenizeResult
- BatchTokenizeResult

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
