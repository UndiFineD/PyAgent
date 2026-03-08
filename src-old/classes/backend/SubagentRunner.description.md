# SubagentRunner

**File**: `src\classes\backend\SubagentRunner.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 366  
**Complexity**: 18 (moderate)

## Overview

Implementation of subagent running logic.

## Classes (1)

### `SubagentRunner`

Handles running subagents with multiple backend support and fallback logic.

**Methods** (18):
- `_resolve_repo_root()`
- `_command_available(command)`
- `__init__(self)`
- `clear_response_cache(self)`
- `get_metrics(self)`
- `reset_metrics(self)`
- `_get_cache_key(self, prompt, model)`
- `validate_response_content(self, response, content_types)`
- `estimate_tokens(self, text)`
- `estimate_cost(self, tokens, model, rate_per_1k_input)`
- ... and 8 more methods

## Dependencies

**Imports** (18):
- `DiskCache.DiskCache`
- `LLMClient.LLMClient`
- `LocalContextRecorder.LocalContextRecorder`
- `RunnerBackends.BackendHandlers`
- `__future__.annotations`
- `hashlib`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `requests`
- `subprocess`
- `time`
- `typing.Any`
- `typing.Dict`
- ... and 3 more

---
*Auto-generated documentation*
