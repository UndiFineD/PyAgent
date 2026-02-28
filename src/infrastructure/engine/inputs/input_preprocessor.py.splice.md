# Splice: src/infrastructure/engine/inputs/input_preprocessor.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- PromptType
- InputFormat
- TextPrompt
- TokensPrompt
- EmbedsPrompt
- EncoderDecoderPrompt
- ChatMessage
- ChatPrompt
- InputMetadata
- ProcessedInput
- PromptTemplate
- PromptValidator
- ConversationLinearizer
- InputPreprocessor

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
