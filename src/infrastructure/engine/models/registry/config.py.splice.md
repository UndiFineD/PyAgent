# Splice: src/infrastructure/engine/models/registry/config.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ModelCapability
- ModelArchitecture
- QuantizationType
- ModelFormat
- ModelConfig
- ArchitectureSpec
- ModelInfo
- VRAMEstimate

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
