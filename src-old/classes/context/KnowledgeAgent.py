#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/KnowledgeAgent.description.md

# KnowledgeAgent

**File**: `src\classes\context\KnowledgeAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 19 imports  
**Lines**: 485  
**Complexity**: 15 (moderate)

## Overview

Agent specializing in Workspace Knowledge and Codebase Context (RAG-lite).

## Classes (1)

### `KnowledgeAgent`

**Inherits from**: BaseAgent

Agent that scans the workspace to provide deep context using MIRIX 6-tier memory.

**Methods** (15):
- `__init__(self, file_path, fleet)`
- `_init_chroma(self)`
- `build_index(self)`
- `record_tier_memory(self, tier, content, metadata)`
- `query_mirix(self, tier, query, limit)`
- `build_vector_index(self)`
- `semantic_search(self, query, n_results)`
- `scan_workspace(self, query)`
- `find_backlinks(self, file_name)`
- `auto_update_backlinks(self, directory)`
- ... and 5 more methods

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `chromadb`
- `datetime.datetime`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.engines.ContextCompressor.ContextCompressor`
- `src.logic.agents.cognitive.context.engines.GraphContextEngine.GraphContextEngine`
- `src.logic.agents.cognitive.context.engines.KnowledgeCore.KnowledgeCore`
- `src.logic.agents.cognitive.context.engines.MemoryEngine.MemoryEngine`
- ... and 4 more

---
*Auto-generated documentation*
## Source: src-old/classes/context/KnowledgeAgent.improvements.md

# Improvements for KnowledgeAgent

**File**: `src\classes\context\KnowledgeAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 485 lines (medium)  
**Complexity**: 15 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `KnowledgeAgent_test.py` with pytest tests

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

r"""Agent specializing in Workspace Knowledge and Codebase Context (RAG-lite)."""
