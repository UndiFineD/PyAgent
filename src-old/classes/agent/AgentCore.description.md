# AgentCore

**File**: `src\classes\agent\AgentCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 125  
**Complexity**: 6 (moderate)

## Overview

AgentCore: Pure logic component for the Agent system.
Handles data transformation, parsing, and decision-making without IO side-effects.
Ready for conversion to a Rust library with strong typing.

## Classes (1)

### `AgentCore`

**Inherits from**: BaseCore

Logic-only core for managing improvement tasks and state.

**Methods** (6):
- `__init__(self, workspace_root, settings)`
- `parse_improvements_content(self, content)`
- `update_fixed_items(self, content, fixed_items)`
- `generate_changelog_entries(self, fixed_items)`
- `score_improvement_items(self, items)`
- `get_agent_command(self, python_exe, script_name, context_file, prompt, strategy)`

## Dependencies

**Imports** (8):
- `base_agent.core.BaseCore`
- `pathlib.Path`
- `re`
- `sys`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
