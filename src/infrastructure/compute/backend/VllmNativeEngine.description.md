# VllmNativeEngine

**File**: `src\infrastructure\compute\backend\VllmNativeEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 116  
**Complexity**: 5 (moderate)

## Overview

High-performance native vLLM engine for PyAgent's 'Own AI'.
Optimized for local inference and future trillion-parameter context handling.

## Classes (1)

### `VllmNativeEngine`

Manages a local vLLM instance using the library directly.
Preferred for 'Own AI' where local hardware is sufficient.

**Methods** (5):
- `__init__(self, model_name, gpu_memory_utilization, tensor_parallel_size)`
- `get_instance(cls)`
- `_init_llm(self)`
- `generate(self, prompt, system_prompt, temperature, max_tokens)`
- `shutdown(self)`

## Dependencies

**Imports** (11):
- `gc`
- `logging`
- `os`
- `torch`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `vllm.LLM`
- `vllm.SamplingParams`

---
*Auto-generated documentation*
