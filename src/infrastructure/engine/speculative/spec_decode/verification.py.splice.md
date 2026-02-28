# Splice: src/infrastructure/engine/speculative/spec_decode/verification.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- VerificationResult
- SpecDecodeVerifier
- BatchVerifier
- StreamingVerifier

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
