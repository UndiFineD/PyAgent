#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/models/communication_models.description.md

# communication_models

**File**: `src\\core\base\\models\\communication_models.py`  
**Type**: Python Module  
**Summary**: 15 classes, 0 functions, 19 imports  
**Lines**: 300  
**Complexity**: 29 (complex)

## Overview

Models for agent communication, prompts, and tracing.

## Classes (15)

### `CascadeContext`

Context for recursive agent delegation (Phase 259/275).
Tracks depth and lineage to prevent infinite loops and provide tracing.

**Methods** (2):
- `next_level(self, agent_id)`
- `is_bursting(self)`

### `PromptTemplate`

reusable prompt template. 

**Methods** (1):
- `render(self)`

### `ConversationMessage`

A message in conversation history.

### `ConversationHistory`

Manages a conversation history with message storage and retrieval.

**Methods** (4):
- `__init__(self, max_messages)`
- `add(self, role, content)`
- `get_context(self)`
- `clear(self)`

### `PromptTemplateManager`

Manages a collection of prompt templates.

**Methods** (3):
- `__init__(self)`
- `register(self, template)`
- `render(self, template_name)`

### `ResponsePostProcessor`

Manages post-processing hooks for agent responses.

**Methods** (3):
- `__init__(self)`
- `register(self, hook, priority)`
- `process(self, text)`

### `PromptVersion`

Versioned prompt for A/B testing.

**Methods** (1):
- `__init__(self, version, content, description, active, version_id, template_id, variant, prompt_text, weight)`

### `BatchRequest`

Request in a batch processing queue.

**Methods** (4):
- `__init__(self, file_path, prompt, priority, callback, max_size)`
- `add(self, item)`
- `size(self)`
- `execute(self, processor)`

### `BatchResult`

Result of a batch processing request.

### `MultimodalInput`

Multimodal input for agents.

### `ContextWindow`

Manages token-based context window.

**Methods** (4):
- `used_tokens(self)`
- `available_tokens(self)`
- `add(self, message, token_count)`
- `clear(self)`

### `MultimodalBuilder`

Builds multimodal input sets.

**Methods** (4):
- `add(self, content, input_type)`
- `add_text(self, content)`
- `add_image(self, content)`
- `build(self)`

### `CachedResult`

A cached agent result.

### `TelemetrySpan`

A telemetry span for tracing.

### `SpanContext`

Context for a telemetry span.

**Methods** (3):
- `__init__(self, span)`
- `set_attribute(self, key, value)`
- `add_event(self, name, attributes)`

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `base_models._empty_dict_str_any`
- `base_models._empty_list_dict_str_any`
- `base_models._empty_list_str`
- `collections.abc.Callable`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enums.AgentEvent`
- `enums.FilePriority`
- `enums.InputType`
- `enums.MessageRole`
- `pathlib.Path`
- `time`
- `typing.Any`
- ... and 4 more

---
*Auto-generated documentation*
## Source: src-old/core/base/models/communication_models.improvements.md

# Improvements for communication_models

**File**: `src\\core\base\\models\\communication_models.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 300 lines (medium)  
**Complexity**: 29 score (complex)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `communication_models_test.py` with pytest tests

### Code Organization
- [TIP] **15 classes in one file** - Consider splitting into separate modules

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

r"""Models for agent communication, prompts, and tracing."""
