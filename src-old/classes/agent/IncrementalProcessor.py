#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/agent/IncrementalProcessor.description.md

# IncrementalProcessor

**File**: `src\\classes\agent\\IncrementalProcessor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 236  
**Complexity**: 11 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `IncrementalProcessor`

Processes only files changed since last run.

Tracks file modification times and content hashes to enable
incremental processing, avoiding reprocessing unchanged files.
Phases 233/271: Uses BLAKE3 and CBOR with buffered reads for performance.

Attributes:
    state_file: Path to state persistence file.
    state: Current incremental processing state.

**Methods** (11):
- `__init__(self, repo_root, state_file)`
- `_load_state(self)`
- `_apply_state_data(self, data)`
- `_save_state(self)`
- `_compute_file_hash(self, file_path)`
- `validate_hashes(self, files)`
- `batch_requests(self, files, token_limit)`
- `get_changed_files(self, files)`
- `mark_processed(self, file_path)`
- `complete_run(self)`
- ... and 1 more methods

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `blake3`
- `cbor2`
- `logging`
- `mmap`
- `orjson`
- `os`
- `pathlib.Path`
- `src.core.base.models.IncrementalState`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/IncrementalProcessor.improvements.md

# Improvements for IncrementalProcessor

**File**: `src\\classes\agent\\IncrementalProcessor.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 236 lines (medium)  
**Complexity**: 11 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `IncrementalProcessor_test.py` with pytest tests

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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

r"""Auto-extracted class from agent.py"""
