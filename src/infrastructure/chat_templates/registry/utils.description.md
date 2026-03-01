# utils

**File**: `src\infrastructure\chat_templates\registry\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 8 functions, 15 imports  
**Lines**: 121  
**Complexity**: 8 (moderate)

## Overview

Utility and convenience functions for chat templates.

## Functions (8)

### `_get_registry()`

Get default registry.

### `_get_resolver()`

Get default resolver.

### `register_template(name, template_string, template_type, model_patterns)`

Register a custom template.

### `get_template(model_name, tokenizer)`

Get template for a model.

### `render_template(messages, model_name, template, template_string, add_generation_prompt)`

Render messages using a template.

### `detect_template_type(model_name)`

Detect template type from model name.

### `_try_rust_render_template(template, messages, add_generation_prompt)`

Try Rust-accelerated template rendering.

### `_try_rust_detect_template(model_name)`

Try Rust-accelerated template detection.

## Dependencies

**Imports** (15):
- `base.ChatTemplate`
- `config.MODEL_TEMPLATE_MAP`
- `config.RenderOptions`
- `config.TemplateConfig`
- `config.TemplateType`
- `jinja.JinjaTemplate`
- `logging`
- `registry.ChatTemplateRegistry`
- `resolver.TemplateResolver`
- `rust_core.detect_chat_template_rust`
- `rust_core.render_jinja_template_rust`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
