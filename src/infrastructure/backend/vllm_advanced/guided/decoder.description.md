# decoder

**File**: `src\infrastructure\backend\vllm_advanced\guided\decoder.py`  
**Type**: Python Module  
**Summary**: 1 classes, 2 functions, 21 imports  
**Lines**: 354  
**Complexity**: 13 (moderate)

## Overview

Guided decoding engine for structured output generation.

## Classes (1)

### `GuidedDecoder`

Guided decoding engine for structured output generation.

**Methods** (11):
- `__init__(self, model, gpu_memory_utilization)`
- `get_instance(cls)`
- `is_available(self)`
- `_ensure_initialized(self)`
- `generate(self, prompt, config, temperature, max_tokens, system_prompt)`
- `generate_json(self, prompt, schema, temperature, max_tokens, system_prompt, parse)`
- `generate_regex(self, prompt, pattern, temperature, max_tokens, system_prompt, validate)`
- `generate_choice(self, prompt, choices, temperature, system_prompt)`
- `generate_grammar(self, prompt, grammar, temperature, max_tokens, system_prompt)`
- `get_stats(self)`
- ... and 1 more methods

## Functions (2)

### `generate_json(prompt, schema, model)`

Convenience function for JSON generation.

### `generate_choice(prompt, choices, model)`

Convenience function for choice generation.

## Dependencies

**Imports** (21):
- `__future__.annotations`
- `gc`
- `json`
- `logging`
- `models.ChoiceConstraint`
- `models.GuidedConfig`
- `models.GuidedMode`
- `models.RegexPattern`
- `os`
- `outlines`
- `re`
- `schema.JsonSchema`
- `torch`
- `typing.Any`
- `typing.Dict`
- ... and 6 more

---
*Auto-generated documentation*
