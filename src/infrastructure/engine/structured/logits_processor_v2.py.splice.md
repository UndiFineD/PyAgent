# Splice: src/infrastructure/engine/structured/logits_processor_v2.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MoveDirectionality
- SamplingParams
- BatchUpdate
- BatchUpdateBuilder
- LogitsProcessor
- MinPLogitsProcessor
- LogitBiasLogitsProcessor
- CompositeLogitsProcessor
- LogitsProcessorRegistry

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
