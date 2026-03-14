#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/MarkdownAgent.description.md

# MarkdownAgent

**File**: `src\classes\coder\MarkdownAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 151  
**Complexity**: 11 (moderate)

## Overview

Agent specializing in Markdown documentation.

## Classes (1)

### `MarkdownAgent`

**Inherits from**: CoderAgent

Agent for Markdown documentation improvement.

**Methods** (11):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `convert_to_wikilinks(self, content)`
- `format_as_callout(self, content, callout_type, title)`
- `ensure_frontmatter(self, content, default_props)`
- `add_mermaid_diagram(self, diagram_type, diagram_definition)`
- `add_dataview_query(self, query)`
- `insert_knowledge_graph(self)`
- `insert_backlinks(self)`
- `convert_to_callouts(self, content)`
- ... and 1 more methods

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `pathlib.Path`
- `re`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.KnowledgeAgent.KnowledgeAgent`
- `src.logic.agents.development.CoderAgent.CoderAgent`
- `yaml`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/MarkdownAgent.improvements.md

# Improvements for MarkdownAgent

**File**: `src\classes\coder\MarkdownAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 151 lines (medium)  
**Complexity**: 11 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MarkdownAgent_test.py` with pytest tests

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

r"""Agent specializing in Markdown documentation."""
