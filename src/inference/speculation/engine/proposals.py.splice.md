# Splice: src/inference/speculation/engine/proposals.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- DraftProposal
- VerificationResult
- SpecDecodingMetrics

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
