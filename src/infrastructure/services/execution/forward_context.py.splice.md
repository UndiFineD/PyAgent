# Splice: src/infrastructure/services/execution/forward_context.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- BatchDescriptor
- DPMetadata
- ForwardContext
- ForwardTimingTracker

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
