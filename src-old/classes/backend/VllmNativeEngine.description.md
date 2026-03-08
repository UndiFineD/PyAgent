# VllmNativeEngine

**File**: `src\classes\backend\VllmNativeEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 252  
**Complexity**: 8 (moderate)

## Overview

High-performance native vLLM engine for PyAgent's 'Own AI'.
Optimized for local inference and future trillion-parameter context handling.

## Classes (1)

### `VllmNativeEngine`

Manages a local vLLM instance using the library directly.
Preferred for 'Own AI' where local hardware is sufficient.

**Methods** (8):
- `__init__(self, model_name, gpu_memory_utilization, tensor_parallel_size)`
- `get_instance(cls)`
- `_init_llm(self)`
- `generate(self, prompt, system_prompt, temperature, max_tokens, lora_request, guided_json, guided_regex, guided_choice)`
- `generate_json(self, prompt, schema, system_prompt, temperature, max_tokens)`
- `generate_choice(self, prompt, choices, system_prompt)`
- `generate_regex(self, prompt, pattern, system_prompt, max_tokens)`
- `shutdown(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `gc`
- `logging`
- `os`
- `src.core.base.Version.VERSION`
- `torch`
- `typing.Any`
- `vllm.LLM`
- `vllm.SamplingParams`

---
*Auto-generated documentation*
