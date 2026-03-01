# backend

**File**: `src\infrastructure\backend\llm_backends\lmstudio\backend.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 24 imports  
**Lines**: 433  
**Complexity**: 15 (moderate)

## Overview

LM Studio LLM backend implementation.

## Classes (1)

### `LMStudioBackend`

**Inherits from**: LLMBackend

LM Studio LLM Backend using the official SDK.

**Methods** (15):
- `__init__(self, session, connectivity_manager, recorder, config)`
- `_check_sdk(self)`
- `_get_client(self)`
- `_get_async_client(self)`
- `disconnect(self)`
- `list_loaded_models(self)`
- `list_downloaded_models(self)`
- `get_model(self, model)`
- `chat(self, prompt, model, system_prompt)`
- `chat_stream(self, prompt, model, system_prompt, on_fragment)`
- ... and 5 more methods

## Dependencies

**Imports** (24):
- `LLMBackend.LLMBackend`
- `cache.ModelCache`
- `lmstudio`
- `logging`
- `models.LMStudioConfig`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Iterator`
- `typing.Optional`
- `typing.Sequence`
- `typing.TYPE_CHECKING`
- ... and 9 more

---
*Auto-generated documentation*
