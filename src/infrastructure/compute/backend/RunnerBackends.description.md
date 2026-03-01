# RunnerBackends

**File**: `src\infrastructure\compute\backend\RunnerBackends.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 178  
**Complexity**: 6 (moderate)

## Overview

Backend implementation handlers for SubagentRunner.

## Classes (1)

### `BackendHandlers`

Namespace for backend execution logic.

**Methods** (6):
- `build_full_prompt(description, prompt, original_content)`
- `try_codex_cli(full_prompt, repo_root)`
- `try_copilot_cli(full_prompt, repo_root)`
- `try_gh_copilot(full_prompt, repo_root, allow_non_command)`
- `try_github_models(full_prompt, requests_lib)`
- `try_openai_api(full_prompt, requests_lib)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `subprocess`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
