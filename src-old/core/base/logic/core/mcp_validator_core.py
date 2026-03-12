#!/usr/bin/env python3
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

"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/mcp_validator_core.description.md

# mcp_validator_core

**File**: `src\\core\base\\logic\\core\\mcp_validator_core.py`  
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
## Source: src-old/core/base/logic/core/mcp_validator_core.improvements.md

# Improvements for mcp_validator_core

**File**: `src\\core\base\\logic\\core\\mcp_validator_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 97 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `mcp_validator_core_test.py` with pytest tests

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

import re
from typing import Any, Dict, List


class McpValidatorCore:
    """Validates MCP (Model Context Protocol) servers and tools for security.

    Harvested from .external/mcp-security:
    - Checks for prompt injection in descriptions.
    - Identifies high-risk tools.
    - Validates cleanup and lifecycle hooks.
    """

    # Indicators of potential prompt injection or malicious instructions
    INJECTION_KEYWORDS = [
        r"ignore previous",
        r"system prompt",
        r"do not disclose",
        r"delete all files",
        r"secret key",
        r"override",
        r"hidden tag",
    ]

    # High-impact tool patterns requiring user confirmation
    HIGH_IMPACT_TOOLS = [
        r"delete",
        r"remove",
        r"format",
        r"execute",
        r"shell",
        r"bash",
        r"send_money",
        r"write_file",
        r"edit_file",
    ]

    def validate_tool_definition(self, tool_def: Dict[str, Any]) -> List[str]:
        """Runs multiple security checks on a tool definition.
        Returns a list of warning messages.
        """
        warnings = []
        name = tool_def.get("name", "unknown")
        description = tool_def.get("description", "")

        # 1. Check for injection keywords in description
        for keyword in self.INJECTION_KEYWORDS:
            if re.search(keyword, description, re.IGNORECASE):
                warnings.append(
                    f"Potential injection trigger in tool '{name}' description: '{keyword}'"
                )

        # 2. Identify high-impact tools
        for pattern in self.HIGH_IMPACT_TOOLS:
            if re.search(pattern, name, re.IGNORECASE):
                warnings.append(
                    f"High-impact tool detected: '{name}'. Requires explicit confirmation."
                )

        return warnings

    def check_metadata_isolation(self, mcp_server_config: Dict[str, Any]) -> bool:
        """Ensures metadata (like API keys) is not exposed in the server schema.
        """

        # Search recursively for 'key', 'secret', 'token' in the config structure
        def find_secrets(obj):
            if isinstance(obj, str):
                if any(x in obj.lower() for x in ["key", "secret", "token"]):
                    return True
            elif isinstance(obj, dict):
                return any(find_secrets(v) for v in obj.values())
            elif isinstance(obj, list):
                return any(find_secrets(v) for v in obj)
            return False

        return not find_secrets(mcp_server_config)

    def validate_environment_variables(self, env_vars: Dict[str, str]) -> List[str]:
        """Checks if environment variables passed to MCP servers are safe."""
        risky_vars = ["PATH", "LD_PRELOAD", "PYTHONPATH"]
        warnings = []
        for var in risky_vars:
            if var in env_vars:
                warnings.append(
                    f"MCP server attempting to override critical env var: {var}"
                )
        return warnings
