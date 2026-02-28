# Splice: src/infrastructure/engine/multimodal/processor/base.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ModalityType
- MultiModalConfig
- PlaceholderInfo
- MultiModalData
- MultiModalInputs
- BaseMultiModalProcessor

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
