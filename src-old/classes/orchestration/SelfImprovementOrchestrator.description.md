# SelfImprovementOrchestrator

**File**: `src\classes\orchestration\SelfImprovementOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 559  
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
- `update_research_report(self, results)`
- `_analyze_and_fix(self, file_path)`
- `_log_results(self, results)`
- `_review_ai_lessons(self)`

## Dependencies

**Imports** (18):
- `ast`
- `glob`
- `gzip`
- `json`
- `logging`
- `os`
- `py_compile`
- `re`
- `requests`
- `src.classes.backend.LLMClient.LLMClient`
- `src.classes.base_agent.BaseAgent`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 3 more

---
*Auto-generated documentation*
