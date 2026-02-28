# Splice: src/core/base/common/multimodal_encoders.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- StreamingVisionEncoder
- StreamingAudioProcessor

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
