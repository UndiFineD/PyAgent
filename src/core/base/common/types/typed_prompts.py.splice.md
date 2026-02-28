# Splice: src/core/base/common/types/typed_prompts.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- TextPrompt
- TokensPrompt
- EmbedsPrompt
- DataPrompt
- ExplicitEncoderDecoderPrompt

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
