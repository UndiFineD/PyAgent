# ModelOptimizerAgent

**File**: `src\classes\specialized\ModelOptimizerAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 106  
**Complexity**: 6 (moderate)

## Overview

Agent specializing in model inference optimization and low-VRAM strategies.

## Classes (1)

### `ModelOptimizerAgent`

**Inherits from**: BaseAgent

Optimizes LLM deployment and inference using patterns like AirLLM.

**Methods** (6):
- `__init__(self, file_path)`
- `select_optimization_strategy(self, model_size_gb, available_vram_gb, hardware_features)`
- `run_tinyml_benchmark(self, model_id, hardware_target)`
- `get_fastflow_command(self, model_tag)`
- `get_airllm_setup_code(self, model_id, compression)`
- `improve_content(self, task_description)`

## Dependencies

**Imports** (9):
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
