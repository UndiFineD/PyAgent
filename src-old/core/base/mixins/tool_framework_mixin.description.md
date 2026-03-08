# tool_framework_mixin

**File**: `src\core\base\mixins\tool_framework_mixin.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 19 imports  
**Lines**: 341  
**Complexity**: 12 (moderate)

## Overview

Tool Framework Mixin for BaseAgent.
Provides schema-based tool creation and management, inspired by Adorable's tool system.

## Classes (5)

### `ToolParameter`

Represents a tool parameter with validation.

**Methods** (1):
- `to_dict(self)`

### `ToolDefinition`

Complete definition of a tool.

**Methods** (1):
- `to_dict(self)`

### `ToolExecutionError`

**Inherits from**: Exception

Exception raised when tool execution fails.

### `ToolValidationError`

**Inherits from**: Exception

Exception raised when tool parameters are invalid.

### `ToolFrameworkMixin`

Mixin providing schema-based tool creation and management.
Inspired by Adorable's tool system with createTool() pattern.

**Methods** (10):
- `__init__(self)`
- `create_tool(self, tool_id, description, parameter_schema, category, version)`
- `get_tool_definitions(self)`
- `get_tool_definition(self, tool_id)`
- `unregister_tool(self, tool_id)`
- `get_tool_stats(self)`
- `_auto_discover_tools(self)`
- `_validate_tool_parameters(self, tool_def, parameters)`
- `_get_type_string(self, type_hint)`
- `_update_tool_stats(self, tool_id, success, error)`

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `asyncio`
- `dataclasses.dataclass`
- `inspect`
- `json`
- `logging`
- `pathlib.Path`
- `pydantic`
- `pydantic.BaseModel`
- `pydantic.Field`
- `pydantic.ValidationError`
- `src.core.base.common.models.communication_models.CascadeContext`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- ... and 4 more

---
*Auto-generated documentation*
