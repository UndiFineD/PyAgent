# Splice: src/infrastructure/engine/prompt_renderer/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- TruncationStrategy
- InputType
- RenderMode
- PromptConfig
- TruncationResult
- RenderResult
- EmbeddingInput
- MultimodalInput

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
