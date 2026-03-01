# chat

**File**: `src\infrastructure\compute\backend\llm_backends\lmstudio\chat.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 210  
**Complexity**: 6 (moderate)

## Overview

LM Studio chat completion handler.

## Classes (1)

### `ChatHandler`

Handler for chat operations with SDK-first and HTTP fallback support.

**Methods** (6):
- `__init__(self, api_client)`
- `_build_prediction_config(self, sdk_available)`
- `_extract_chat_from_lmstudio(self, system_prompt)`
- `_sdk_chat(self, llm, prompt, system_prompt)`
- `_http_fallback_chat(self, prompt, model, system_prompt)`
- `chat(self, llm, prompt, model, system_prompt, sdk_available)`

## Dependencies

**Imports** (12):
- `api.LMStudioAPIClient`
- `httpx`
- `lmstudio`
- `logging`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
