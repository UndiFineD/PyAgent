# cli

**File**: `src\classes\agent\cli.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 13 imports  
**Lines**: 251  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for cli.

## Functions (3)

### `_parse_quick_flag(val)`

format 'provider:model' or 'model'

### `parse_model_overrides(raw_list)`

Parse repeatable `--model` entries of form `agent=provider:model` or `agent=model`.

Returns mapping agent -> spec dict.

### `main()`

CLI entry point for the Agent Orchestrator.

## Dependencies

**Imports** (13):
- `Agent.Agent`
- `HealthChecker.HealthChecker`
- `RateLimitConfig.RateLimitConfig`
- `argparse`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `sys`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `utils.setup_logging`

---
*Auto-generated documentation*
