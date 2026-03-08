# TemplateManager

**File**: `src\core\base\utils\TemplateManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 90  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `TemplateManager`

Manage agent templates for common use cases.

Example:
    manager=TemplateManager()
    manager.add_template(AgentTemplate(
        name = "python_cleanup",
        agents = ["coder", "tests"],
        file_patterns = ["*.py"],
    ))

    template=manager.get_template("python_cleanup")
    agent=template_to_agent(template)

**Methods** (5):
- `__init__(self)`
- `_register_defaults(self)`
- `add_template(self, template)`
- `get_template(self, name)`
- `list_templates(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.utils.AgentTemplate.AgentTemplate`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
