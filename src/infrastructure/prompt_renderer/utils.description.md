# utils

**File**: `src\infrastructure\prompt_renderer\utils.py`  
**Type**: Python Module  
**Summary**: 1 classes, 6 functions, 21 imports  
**Lines**: 181  
**Complexity**: 9 (moderate)

## Overview

Utility functions and loaders for prompt rendering.

## Classes (1)

### `EmbeddingLoader`

Load embeddings from various formats.

**Methods** (3):
- `load_base64(cls, data, encoding)`
- `load_file(cls, path, encoding)`
- `to_base64(cls, embeddings, encoding)`

## Functions (6)

### `render_prompt(prompt, messages, tokenizer, max_tokens, truncation, chat_template)`

Render a prompt with automatic mode detection.

### `apply_chat_template(messages, template, tokenizer, add_generation_prompt)`

Apply chat template to messages.

### `truncate_prompt(tokens, max_tokens, strategy, reserve_tokens)`

Truncate token sequence.

### `generate_cache_salt(chat_template, add_special_tokens)`

Generate cache salt for configuration.

### `_try_rust_render_template(template, messages, add_generation_prompt)`

Try Rust-accelerated template rendering.

### `_try_rust_find_placeholders(text, patterns)`

Try Rust-accelerated placeholder finding.

## Dependencies

**Imports** (21):
- `__future__.annotations`
- `base64`
- `models.EmbeddingInput`
- `models.PromptConfig`
- `models.RenderResult`
- `models.TruncationResult`
- `models.TruncationStrategy`
- `renderers.ChatRenderer`
- `renderers.CompletionRenderer`
- `rust_core.find_placeholders_rust`
- `rust_core.render_chat_template_rust`
- `salt.CacheSaltGenerator`
- `struct`
- `truncation.TruncationManager`
- `typing.Any`
- ... and 6 more

---
*Auto-generated documentation*
