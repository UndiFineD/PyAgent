# InputPreprocessor

**File**: `src\infrastructure\inputs\InputPreprocessor.py`  
**Type**: Python Module  
**Summary**: 14 classes, 2 functions, 20 imports  
**Lines**: 644  
**Complexity**: 35 (complex)

## Overview

InputPreprocessor: Unified input processing with schema validation.

Provides:
- Type-safe prompt schemas (text, tokens, embeddings)
- Encoder-decoder prompt separation
- Multi-turn conversation linearization
- Embedding cache integration
- Input size estimation for batch scheduling

## Classes (14)

### `PromptType`

**Inherits from**: Enum

Types of prompt input.

### `InputFormat`

**Inherits from**: Enum

Input format specifications.

### `TextPrompt`

Text-based prompt.

**Methods** (2):
- `type(self)`
- `__len__(self)`

### `TokensPrompt`

Pre-tokenized prompt.

**Methods** (2):
- `type(self)`
- `__len__(self)`

### `EmbedsPrompt`

Pre-computed embeddings prompt.

**Methods** (2):
- `type(self)`
- `__len__(self)`

### `EncoderDecoderPrompt`

Prompt for encoder-decoder models (T5, BART, etc.).

**Methods** (1):
- `type(self)`

### `ChatMessage`

Single message in a conversation.

**Methods** (1):
- `to_dict(self)`

### `ChatPrompt`

Multi-turn conversation prompt.

**Methods** (2):
- `type(self)`
- `__len__(self)`

### `InputMetadata`

Metadata about processed input.

### `ProcessedInput`

Fully processed input ready for model.

**Methods** (1):
- `length(self)`

### `PromptTemplate`

Template for formatting prompts.

**Methods** (1):
- `get_template(cls, format)`

### `PromptValidator`

Validates prompt inputs.

**Methods** (7):
- `__init__(self, max_length, allow_empty, require_user_message)`
- `validate(self, prompt)`
- `_validate_text(self, prompt)`
- `_validate_tokens(self, prompt)`
- `_validate_embeds(self, prompt)`
- `_validate_chat(self, prompt)`
- `_validate_encoder_decoder(self, prompt)`

### `ConversationLinearizer`

Linearizes multi-turn conversations to single prompt.

Supports multiple chat formats (ChatML, Llama, Anthropic, etc.)

**Methods** (3):
- `__init__(self, format, add_generation_prompt)`
- `linearize(self, chat)`
- `parse_messages(self, text)`

### `InputPreprocessor`

Unified input preprocessing for LLM inference.

Features beyond vLLM:
- JSON Schema validation for structured inputs
- Automatic prompt template detection
- Multi-turn conversation linearization
- Embedding cache integration
- Input size estimation for scheduling

**Methods** (11):
- `__init__(self, tokenizer, default_format, max_length, truncation, estimate_chars_per_token)`
- `process(self, prompt)`
- `_process_text(self, prompt)`
- `_process_tokens(self, prompt)`
- `_process_embeds(self, prompt)`
- `_process_chat(self, prompt)`
- `_process_encoder_decoder(self, prompt)`
- `_estimate_tokens(self, text)`
- `detect_format(self, text)`
- `batch_process(self, prompts)`
- ... and 1 more methods

## Functions (2)

### `parse_prompt(prompt)`

Parse various input formats to typed prompt.

### `estimate_tokens(text, chars_per_token)`

Estimate token count from text length.

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `numpy`
- `re`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Generator`
- `typing.Iterator`
- ... and 5 more

---
*Auto-generated documentation*
