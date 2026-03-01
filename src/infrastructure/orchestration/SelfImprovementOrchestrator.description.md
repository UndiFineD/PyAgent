# SelfImprovementOrchestrator

**File**: `src\infrastructure\orchestration\SelfImprovementOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 21 imports  
**Lines**: 603  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for SelfImprovementOrchestrator.

## Classes (1)

### `SelfImprovementOrchestrator`

**Inherits from**: BaseAgent

Orchestrates the fleet's self-improvement cycle: scanning for tech debt, 
security leaks, and quality issues, and applying autonomous fixes.

**Methods** (6):
- `__init__(self, fleet_manager)`
- `run_improvement_cycle(self, target_dir)`
- `update_research_report(self, results, lessons)`
- `_analyze_and_fix(self, file_path)`
- `_log_results(self, results)`
- `_review_ai_lessons(self)`

## Dependencies

**Imports** (21):
- `__future__.annotations`
- `ast`
- `glob`
- `gzip`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `py_compile`
- `re`
- `requests`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.STABILITY_SCORE`
- `src.core.base.version.VERSION`
- `src.core.base.version.is_gate_open`
- ... and 6 more

---
*Auto-generated documentation*
