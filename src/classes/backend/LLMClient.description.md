# LLMClient

**File**: `src\classes\backend\LLMClient.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 348  
**Complexity**: 12 (moderate)

## Overview

Centralized LLM client for various backends.

## Classes (1)

### `LLMClient`

Handles direct HTTP calls to LLM providers.

**Methods** (12):
- `__init__(self, requests_lib, workspace_root)`
- `_get_cache_key(self, provider, model, prompt, system_prompt)`
- `_load_conn_status(self)`
- `_save_conn_status(self)`
- `_is_connection_working(self, provider_id)`
- `_update_connection_status(self, provider_id, working)`
- `_record(self, provider, model, prompt, result, system_prompt)`
- `llm_chat_via_github_models(self, prompt, model, system_prompt, base_url, token, timeout_s, max_retries, stream)`
- `llm_chat_via_ollama(self, prompt, model, system_prompt, base_url, timeout_s)`
- `llm_chat_via_vllm(self, prompt, model, system_prompt, base_url, timeout_s)`
- ... and 2 more methods

## Dependencies

**Imports** (17):
- `LocalContextRecorder.LocalContextRecorder`
- `VllmNativeEngine.VllmNativeEngine`
- `__future__.annotations`
- `base_agent.ConnectivityManager.ConnectivityManager`
- `functools.lru_cache`
- `hashlib`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `threading`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 2 more

---
*Auto-generated documentation*
