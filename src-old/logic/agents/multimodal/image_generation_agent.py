#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/multimodal/image_generation_agent.description.md

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
## Source: src-old/logic/agents/multimodal/image_generation_agent.improvements.md

# Improvements for image_generation_agent

**File**: `src\logic\agents\multimodal\image_generation_agent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 140 lines (medium)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `image_generation_agent_test.py` with pytest tests

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

from __future__ import annotations

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

"""
Image Generation Agent for PyAgent.
Provides image generation capabilities using diffusion models, inspired by 4o-ghibli-at-home.
"""


import os
import time
from typing import Any, Dict, Optional
from pathlib import Path

try:
    from PIL import Image
    import torch
    from diffusers import FluxPipeline

    HAS_DIFFUSERS = True
except ImportError:
    Image = None
    torch = None
    FluxPipeline = None
    HAS_DIFFUSERS = False

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.mixins.task_queue_mixin import TaskQueueMixin


class ImageGenerationAgent(BaseAgent, TaskQueueMixin):
    """
    Agent for generating images using diffusion models.
    Supports async processing with memory management.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        TaskQueueMixin.__init__(self, **kwargs)

        self.model_name = kwargs.get("model_name", "black-forest-labs/FLUX.1-dev")
        self.device = kwargs.get(
            "device", "cuda" if (torch and torch.cuda.is_available()) else "cpu"
        )
        self.output_dir = Path(kwargs.get("output_dir", "generated_images"))
        self.output_dir.mkdir(exist_ok=True)

        self.pipe: Optional[Any] = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the diffusion model with memory optimizations."""
        if not HAS_DIFFUSERS:
            raise ImportError("diffusers and PIL are required for image generation")

        if torch is None:
            raise ImportError("torch not available")

        try:
            self.pipe = FluxPipeline.from_pretrained(
                self.model_name,
                torch_dtype=torch.bfloat16 if self.device == "cuda" else torch.float32,
            )

            if self.device == "cuda":
                self.pipe.enable_model_cpu_offload()
            else:
                self.pipe.to(self.device)

            print(f"Model loaded successfully on {self.device}")

        except Exception as e:
            print(f"Failed to load model: {e}")
            self.pipe = None

    async def generate_image(self, prompt: str, **kwargs: Any) -> str:
        """
        Submit an image generation task.
        Returns job_id for status tracking.
        """
        if not self.pipe:
            raise RuntimeError("Model not loaded")

        task_data = {
            "prompt": prompt,
            "width": kwargs.get("width", 1024),
            "height": kwargs.get("height", 1024),
            "num_inference_steps": kwargs.get("steps", 28),
            "guidance_scale": kwargs.get("guidance_scale", 2.5),
        }

        return await self.submit_task(task_data)

    async def _process_task(self, task_data: Dict[str, Any]) -> str:
        """Process the image generation task."""
        if not self.pipe:
            raise RuntimeError("Model not available")

        try:
            # Generate image
            result = self.pipe(
                prompt=task_data["prompt"],
                width=task_data["width"],
                height=task_data["height"],
                num_inference_steps=task_data["num_inference_steps"],
                guidance_scale=task_data["guidance_scale"],
            )

            image = result.images[0]

            # Save image
            job_id = task_data["job_id"]
            output_path = self.output_dir / f"{job_id}.png"
            image.save(output_path)

            return str(output_path)

        except Exception as e:
            # Check if it's an OOM error
            if hasattr(e, "__class__") and "OutOfMemoryError" in str(type(e)):
                raise RuntimeError("GPU memory insufficient. Try smaller image size.")
            raise RuntimeError(f"Image generation failed: {e}")

    async def get_generated_image(self, job_id: str) -> Optional[Image.Image]:
        """Get the generated image if completed."""
        status = await self.get_task_status(job_id)
        if status and status.get("status") == "completed":
            path = status.get("result")
            if path and Path(path).exists():
                return Image.open(path)
        return None
