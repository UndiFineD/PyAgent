# SubagentCore

**File**: `src\infrastructure\backend\SubagentCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 208  
**Complexity**: 3 (simple)

## Overview

Core execution logic for SubagentRunner.

## Classes (1)

### `SubagentCore`

Delegated execution core for SubagentRunner.

**Methods** (3):
- `__init__(self, runner)`
- `run_subagent(self, description, prompt, original_content)`
- `llm_chat_via_github_models(self, prompt, model, system_prompt, base_url, token, timeout_s, max_retries, use_cache, stream, validate_content)`

## Dependencies

**Imports** (9):
- `RunnerBackends.BackendHandlers`
- `SubagentRunner.SubagentRunner`
- `__future__.annotations`
- `logging`
- `os`
- `rust_core`
- `src.core.base.Version.VERSION`
- `time`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
