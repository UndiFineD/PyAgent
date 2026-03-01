# registry

**File**: `src\infrastructure\chat_templates\registry\registry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 129  
**Complexity**: 10 (moderate)

## Overview

Central template registry.

## Classes (1)

### `ChatTemplateRegistry`

Registry for chat templates with dynamic resolution.

**Methods** (10):
- `__new__(cls)`
- `_initialize_builtins(self)`
- `templates(self)`
- `register(self, name, template, model_patterns)`
- `register_config(self, name, config, model_patterns)`
- `register_resolver(self, resolver)`
- `get(self, name, default)`
- `resolve(self, model_name, tokenizer)`
- `list_templates(self)`
- `unregister(self, name)`

## Dependencies

**Imports** (14):
- `base.ChatTemplate`
- `config.BUILTIN_TEMPLATES`
- `config.MODEL_TEMPLATE_MAP`
- `config.TemplateConfig`
- `config.TemplateInfo`
- `config.TemplateType`
- `jinja.JinjaTemplate`
- `logging`
- `threading`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
