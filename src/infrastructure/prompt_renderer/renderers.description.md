# renderers

**File**: `src\infrastructure\prompt_renderer\renderers.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 19 imports  
**Lines**: 199  
**Complexity**: 5 (moderate)

## Overview

Core renderers for prompt rendering.

## Classes (2)

### `CompletionRenderer`

**Inherits from**: PromptRenderer

Renderer for completion-style prompts.

**Methods** (1):
- `render(self, config)`

### `ChatRenderer`

**Inherits from**: PromptRenderer

Renderer for chat-style prompts.

**Methods** (4):
- `render(self, config)`
- `_apply_template(self, messages, template, add_generation_prompt)`
- `_simple_template(self, messages, add_generation_prompt)`
- `_find_image_positions(self, text, images)`

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `base.PromptRenderer`
- `jinja2.BaseLoader`
- `jinja2.Environment`
- `logging`
- `models.InputType`
- `models.PromptConfig`
- `models.RenderResult`
- `models.TruncationResult`
- `salt.CacheSaltGenerator`
- `truncation.TruncationManager`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 4 more

---
*Auto-generated documentation*
