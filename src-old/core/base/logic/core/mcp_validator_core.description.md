# mcp_validator_core

**File**: `src\core\base\logic\core\mcp_validator_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 97  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for mcp_validator_core.

## Classes (1)

### `McpValidatorCore`

Validates MCP (Model Context Protocol) servers and tools for security.

Harvested from .external/mcp-security:
- Checks for prompt injection in descriptions.
- Identifies high-risk tools.
- Validates cleanup and lifecycle hooks.

**Methods** (3):
- `validate_tool_definition(self, tool_def)`
- `check_metadata_isolation(self, mcp_server_config)`
- `validate_environment_variables(self, env_vars)`

## Dependencies

**Imports** (5):
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
