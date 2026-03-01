# GuidanceBackend

**File**: `src\infrastructure\structured_output\GuidanceBackend.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 26 imports  
**Lines**: 495  
**Complexity**: 30 (complex)

## Overview

GuidanceBackend - Guidance library integration for structured output.

Implements structured output using the Guidance library with:
- Template-based generation
- Stateful tracking
- Async compilation
- Multi-model support

Beyond vLLM innovations:
- Grammar composition
- Template caching
- Variable interpolation
- Streaming token support

## Classes (8)

### `GuidanceTemplateType`

**Inherits from**: Enum

Types of Guidance templates.

### `GuidanceVariable`

Variable in a Guidance template.

**Methods** (1):
- `to_pattern(self)`

### `GuidanceTemplate`

Guidance template specification.

Represents a template with embedded generation instructions.

**Methods** (5):
- `__post_init__(self)`
- `_parse_template(self)`
- `_compute_cache_key(self)`
- `get_prefix_text(self)`
- `get_variable_sequence(self)`

### `GuidanceState`

State for Guidance template execution.

Tracks current position in template and variable values.

**Methods** (4):
- `__init__(self, template)`
- `accept_token(self, token_text)`
- `get_allowed_tokens(self, vocab_size)`
- `reset(self)`

### `CompiledGuidanceProgram`

Compiled Guidance program.

Represents a compiled and ready-to-execute Guidance template.

**Methods** (4):
- `__init__(self, template, vocab_size)`
- `create_state(self)`
- `fill_bitmask(self, state, bitmask)`
- `is_terminated(self, state)`

### `GuidanceGrammar`

Grammar wrapper for Guidance programs.

Provides the standard grammar interface while wrapping
a Guidance program and state.

**Methods** (8):
- `__init__(self, program, tokenizer, state)`
- `accept_token(self, token_id)`
- `accept_token_text(self, text)`
- `fill_next_token_bitmask(self, bitmask)`
- `is_terminated(self)`
- `reset(self)`
- `get_variable_values(self)`
- `create_state(self)`

### `GuidanceBackend`

Guidance library backend for structured output.

Provides template-based constrained generation using the
Guidance library's approach to structured output.

**Methods** (8):
- `__init__(self, tokenizer, vocab_size, max_cache_size)`
- `_get_vocab_size(self, tokenizer)`
- `compile_template(self, template_str, variables)`
- `compile_json_schema(self, schema)`
- `_schema_to_template(self, schema)`
- `allocate_bitmask(self, batch_size)`
- `get_stats(self)`
- `clear_cache(self)`

### `AsyncGuidanceBackend`

**Inherits from**: GuidanceBackend

Async-enabled Guidance backend.

Provides async template compilation for non-blocking operation.

## Dependencies

**Imports** (26):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `hashlib`
- `json`
- `numpy`
- `re`
- `rust_core`
- `threading`
- `time`
- `typing.Any`
- ... and 11 more

---
*Auto-generated documentation*
