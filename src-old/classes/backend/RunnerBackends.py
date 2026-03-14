#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/backend/RunnerBackends.description.md

# RunnerBackends

**File**: `src\\classes\backend\\RunnerBackends.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 232  
**Complexity**: 7 (moderate)

## Overview

Backend implementation handlers for SubagentRunner.

## Classes (1)

### `BackendHandlers`

Namespace for backend execution logic.

**Methods** (7):
- `_parse_content(text)`
- `build_full_prompt(description, prompt, original_content)`
- `try_codex_cli(full_prompt, repo_root, recorder)`
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
- `re`
- `src.core.base.version.VERSION`
- `subprocess`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/backend/RunnerBackends.improvements.md

# Improvements for RunnerBackends

**File**: `src\\classes\backend\\RunnerBackends.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 232 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `RunnerBackends_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""
from __future__ import annotations


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


r"""Backend implementation handlers for SubagentRunner."""
