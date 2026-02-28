# Splice: src/infrastructure/services/mediaio/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MediaType
- ImageFormat
- VideoFormat
- AudioFormat
- ResizeMode
- MediaMetadata
- ImageData
- VideoData
- AudioData
- MediaLoadConfig

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
