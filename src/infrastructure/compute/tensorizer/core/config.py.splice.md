# Splice: src/infrastructure/compute/tensorizer/core/config.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- TensorDtype
- CompressionType
- TensorizerConfig

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
