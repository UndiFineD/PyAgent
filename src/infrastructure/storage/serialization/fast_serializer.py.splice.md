# Splice: src/infrastructure/storage/serialization/fast_serializer.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- SerializationFormat
- SerializerStats
- Serializer
- JSONSerializer
- PickleSerializer
- MsgPackSerializer
- CBORSerializer
- BinarySerializer
- SerializerRegistry

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
