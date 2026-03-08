# image_generation_agent

**File**: `src\logic\agents\multimodal\image_generation_agent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 140  
**Complexity**: 2 (simple)

## Overview

Image Generation Agent for PyAgent.
Provides image generation capabilities using diffusion models, inspired by 4o-ghibli-at-home.

## Classes (1)

### `ImageGenerationAgent`

**Inherits from**: BaseAgent, TaskQueueMixin

Agent for generating images using diffusion models.
Supports async processing with memory management.

**Methods** (2):
- `__init__(self)`
- `_load_model(self)`

## Dependencies

**Imports** (12):
- `PIL.Image`
- `__future__.annotations`
- `diffusers.FluxPipeline`
- `os`
- `pathlib.Path`
- `src.core.base.lifecycle.base_agent.BaseAgent`
- `src.core.base.mixins.task_queue_mixin.TaskQueueMixin`
- `time`
- `torch`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
