# run_fleet_self_improvement

**File**: `src\infrastructure\dev\scripts\run_fleet_self_improvement.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 22 imports  
**Lines**: 453  
**Complexity**: 4 (simple)

## Overview

Autonomous Fleet Self-Improvement Loop.
Scans the workspace for issues, applies autonomous fixes, and harvests external intelligence.

## Functions (4)

### `run_cycle(fleet, root, prompt_path, context_path, current_cycle, model_name)`

Run a single improvement cycle.

### `consult_external_models(fleet, broken_items, prompt_path, model_name)`

Queries external model backends (Ollama, Gemini, and Agentic Copilot) 
to extract lessons for the fleet.

### `_cycle_throttle(delay, root, target_dirs)`

Implement a controlled delay between improvement cycles.
Uses 'watchfiles' for event-driven triggering if available (Phase 147).

### `main()`

## Dependencies

**Imports** (22):
- `__future__.annotations`
- `argparse`
- `dotenv.load_dotenv`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `re`
- `requests`
- `shlex`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LLMClient.LLMClient`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `subprocess`
- `sys`
- ... and 7 more

---
*Auto-generated documentation*
