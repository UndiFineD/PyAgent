# jinja

**File**: `src\infrastructure\chat_templates\registry\jinja.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 126  
**Complexity**: 6 (moderate)

## Overview

Jinja2 template implementations.

## Classes (1)

### `JinjaTemplate`

**Inherits from**: ChatTemplate

Jinja2-based chat template.

**Methods** (6):
- `__init__(self, config)`
- `get_template_string(self)`
- `_get_env(self)`
- `_get_template(self)`
- `render(self, messages, options)`
- `_fallback_render(self, messages, options)`

## Dependencies

**Imports** (13):
- `base.ChatTemplate`
- `config.BUILTIN_TEMPLATES`
- `config.RenderOptions`
- `config.TemplateConfig`
- `config.TemplateType`
- `jinja2.BaseLoader`
- `jinja2.Environment`
- `jinja2.StrictUndefined`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
