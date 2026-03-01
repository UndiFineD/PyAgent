# chat_stream

**File**: `src\infrastructure\compute\backend\llm_backends\lmstudio\chat_stream.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 230  
**Complexity**: 6 (moderate)

## Overview

LM Studio streaming chat completion handler.

## Classes (1)

### `StreamingChatHandler`

Handler for streaming chat operations with SDK-first and HTTP fallback support.

**Methods** (6):
- `__init__(self, api_client)`
- `_build_prediction_config(self, sdk_available)`
- `_extract_chat_from_lmstudio(self, system_prompt)`
- `_sdk_chat_stream(self, llm, prompt, system_prompt, on_fragment)`
- `_http_fallback_chat_stream(self, prompt, model, system_prompt, on_fragment)`
- `chat_stream(self, llm, prompt, model, system_prompt, sdk_available, on_fragment)`

## Dependencies

**Imports** (14):
- `api.LMStudioAPIClient`
- `httpx`
- `json`
- `lmstudio`
- `logging`
- `sseclient`
- `typing.Any`
- `typing.Callable`
- `typing.Iterator`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
