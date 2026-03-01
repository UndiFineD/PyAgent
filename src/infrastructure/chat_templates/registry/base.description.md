# base

**File**: `src\infrastructure\chat_templates\registry\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 51  
**Complexity**: 6 (moderate)

## Overview

Abstract base classes for chat templates.

## Classes (1)

### `ChatTemplate`

**Inherits from**: ABC

Abstract base class for chat templates.

**Methods** (6):
- `__init__(self, config)`
- `template_type(self)`
- `template_hash(self)`
- `get_template_string(self)`
- `render(self, messages, options)`
- `get_info(self)`

## Dependencies

**Imports** (11):
- `abc.ABC`
- `abc.abstractmethod`
- `config.RenderOptions`
- `config.TemplateConfig`
- `config.TemplateInfo`
- `config.TemplateType`
- `hashlib`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
