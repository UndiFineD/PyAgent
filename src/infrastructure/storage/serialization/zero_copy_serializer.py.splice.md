# Splice: src/infrastructure/storage/serialization/zero_copy_serializer.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ZeroCopyEncoder
- ZeroCopyDecoder

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
