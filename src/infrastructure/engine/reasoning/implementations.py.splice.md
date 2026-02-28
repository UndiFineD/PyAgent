# Splice: src/infrastructure/engine/reasoning/implementations.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- DeepSeekReasoningParser
- QwenReasoningParser
- GenericReasoningParser
- OpenAIToolParser
- HermesToolParser

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
