# Splice: src/infrastructure/compute/backend/vllm_advanced/lora/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- AdapterState
- LoraConfig
- LoraAdapter

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
