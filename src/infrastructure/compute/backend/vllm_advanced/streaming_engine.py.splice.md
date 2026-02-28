# Splice: src/infrastructure/compute/backend/vllm_advanced/streaming_engine.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- StreamCallback
- StreamingConfig
- StreamToken
- TokenStreamIterator
- StreamingVllmEngine

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
