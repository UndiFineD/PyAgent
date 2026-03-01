# run_fleet_self_improvement

**File**: `src\infrastructure\dev\scripts\analysis\run_fleet_self_improvement.py`  
**Type**: Python Module  
**Summary**: 3 classes, 11 functions, 19 imports  
**Lines**: 459  
**Complexity**: 20 (complex)

## Overview

Autonomous Fleet Self-Improvement Loop.
Scans the workspace for issues, applies autonomous fixes, and harvests external intelligence.

## Classes (3)

### `DirectiveParser`

Parses strategic directives from prompt and context files.

**Methods** (4):
- `__init__(self, root, prompt_path, context_path)`
- `load_directives(self)`
- `get_focus_dirs(self)`
- `execute_commands(self)`

### `IntelligenceHarvester`

Orchestrates external intelligence harvesting.

**Methods** (2):
- `__init__(self, fleet, model_name)`
- `harvest(self)`

### `CycleOrchestrator`

Manages the execution of multiple improvement cycles.

**Methods** (3):
- `__init__(self, fleet, args)`
- `run(self)`
- `_get_last_focus(self)`

## Functions (11)

### `run_cycle(fleet, root, logger, prompt_path, context_path, current_cycle, model_name)`

Run a single improvement cycle.

### `consult_external_models(fleet, broken_items, prompt_path, model_name)`

Placeholder for federated learning consultation (Phase 112).

### `_analyze_unfixed_issues(stats)`

Filters and summarizes issues that were not fixed.

### `_update_auto_documentation(fleet, root, stats)`

Updates FLEET_AUTO_DOC.md with cycle results.

### `_log_explainability(fleet, stats)`

Logs the reasoning for the improvement cycle.

### `_verify_ai_recording(fleet)`

Verifies that local interaction recording is functional.

### `_synthesize_collective_knowledge(fleet)`

Triggers knowledge synthesis from the swarm.

### `_prune_verified_directives(prompt_path, root, target_dirs, broken_items)`

Removes completed directives from the prompt file.

### `_report_remaining_debt(stats, logger, fleet, root, target_dirs, prompt_path, model_name, current_cycle)`

Logs issues that were not autonomously fixed and performs maintenance.

### `_cycle_throttle(delay, root, target_dirs, use_watcher)`

Implement a controlled delay between improvement cycles.
Uses 'watchfiles' for event-driven triggering if available and requested (Phase 147).

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `argparse`
- `dotenv.load_dotenv`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `re`
- `shlex`
- `src.core.base.Version.VERSION`
- `src.infrastructure.backend`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `src.observability.StructuredLogger.StructuredLogger`
- `subprocess`
- `sys`
- ... and 4 more

---
*Auto-generated documentation*
