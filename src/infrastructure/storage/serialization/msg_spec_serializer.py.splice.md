# Splice: src/infrastructure/storage/serialization/msg_spec_serializer.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- JSONEncoder
- MsgPackEncoder
- TypedSerializer
- BenchmarkResult

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
