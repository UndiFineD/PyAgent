# TypedPrompts

**File**: `src\core\base\types\TypedPrompts.py`  
**Type**: Python Module  
**Summary**: 5 classes, 15 functions, 9 imports  
**Lines**: 472  
**Complexity**: 15 (moderate)

## Overview

TypedPrompts - Type-safe prompt schemas with type guards.

Inspired by vLLM's inputs.data module for type-safe prompt handling
with TypedDict schemas and TypeIs type guards.

Phase 24: Advanced Observability & Parsing

## Classes (5)

### `TextPrompt`

**Inherits from**: TypedDict

Schema for a text prompt.

The text will be tokenized before passing to the model.

### `TokensPrompt`

**Inherits from**: TypedDict

Schema for a pre-tokenized prompt.

Token IDs are passed directly to the model.

### `EmbedsPrompt`

**Inherits from**: TypedDict

Schema for a prompt provided via embeddings.

Pre-computed embeddings are passed directly to the model.

### `DataPrompt`

**Inherits from**: TypedDict

Schema for generic data prompts.

Used for custom IO processor plugins.

### `ExplicitEncoderDecoderPrompt`

**Inherits from**: TypedDict, Unknown

Schema for encoder/decoder model prompts.

Allows specifying separate encoder and decoder prompts.

## Functions (15)

### `is_text_prompt(prompt)`

Check if prompt is a TextPrompt.

Args:
    prompt: Prompt to check
    
Returns:
    True if prompt is a TextPrompt dict

### `is_tokens_prompt(prompt)`

Check if prompt is a TokensPrompt.

Args:
    prompt: Prompt to check
    
Returns:
    True if prompt is a TokensPrompt dict

### `is_embeds_prompt(prompt)`

Check if prompt is an EmbedsPrompt.

Args:
    prompt: Prompt to check
    
Returns:
    True if prompt is an EmbedsPrompt dict

### `is_data_prompt(prompt)`

Check if prompt is a DataPrompt.

Args:
    prompt: Prompt to check
    
Returns:
    True if prompt is a DataPrompt dict

### `is_string_prompt(prompt)`

Check if prompt is a plain string.

Args:
    prompt: Prompt to check
    
Returns:
    True if prompt is a string

### `is_explicit_encoder_decoder_prompt(prompt)`

Check if prompt is an ExplicitEncoderDecoderPrompt.

Args:
    prompt: Prompt to check
    
Returns:
    True if prompt has encoder_prompt and decoder_prompt keys

### `parse_prompt(prompt)`

Parse a prompt into a normalized dictionary.

Args:
    prompt: Prompt in any supported format
    
Returns:
    Normalized prompt dict with 'type' and prompt data

### `get_prompt_text(prompt)`

Extract text from a prompt if available.

Args:
    prompt: Prompt to extract text from
    
Returns:
    Prompt text or None if not available

### `get_prompt_token_ids(prompt)`

Extract token IDs from a prompt if available.

Args:
    prompt: Prompt to extract tokens from
    
Returns:
    Token IDs or None if not available

### `has_multi_modal_data(prompt)`

Check if a prompt has multi-modal data.

Args:
    prompt: Prompt to check
    
Returns:
    True if prompt has multi_modal_data

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `typing.Any`
- `typing.Generic`
- `typing.Literal`
- `typing.TypeAlias`
- `typing.TypeVar`
- `typing_extensions.NotRequired`
- `typing_extensions.TypeIs`
- `typing_extensions.TypedDict`

---
*Auto-generated documentation*
