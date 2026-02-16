#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""ImageGenerationAgent - Image generation via diffusion models

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate and use asynchronously:
  from image_generation_agent import ImageGenerationAgent
  agent = ImageGenerationAgent(model_name='black-forest-labs/FLUX.1-dev', device='cuda', output_dir='generated_images')'  job_id = await agent.generate_image("A serene forest in Studio Ghibli style")"  image = await agent.get_generated_image(job_id)

WHAT IT DOES:
- Loads a FluxPipeline diffusion model (diffusers) with memory optimizations (CPU offload when CUDA is available).
- Exposes an async generate_image(prompt, ...) API that enqueues tasks via TaskQueueMixin and returns a job_id for status tracking.
- Processes tasks asynchronously in _process_task: runs the pipeline to produce an Image, saves the resulting PNG to output_dir named by job_id, and returns the saved path.
- Provides basic OOM detection and raises informative RuntimeErrors; allows retrieval of completed results with get_generated_image which returns a PIL Image if available.
- Falls back with clear ImportError when required libraries (PIL, torch, diffusers) are missing.

WHAT IT SHOULD DO BETTER:
- Robust dependency handling and graceful degraded operation (e.g., clear install instructions or fallback stubs) and stronger runtime checks for device/dtype compatibility.
- More granular memory and performance controls: dynamic batch/size adaptation, mixed-precision toggles, scheduler configuration, and configurable offload strategies for large models.
- Better error classification and retry/backoff strategies for transient failures, explicit support for CPU-only inference paths, and clearer telemetry/logging (use logging module instead of print).
- Validate and sanitize input (prompt length, unsupported characters), enforce safe defaults for width/height/steps, and provide progress reporting or streaming outputs for long-running generations.
- Add unit/integration tests, type hints for pipeline internals, and clearer public API docs and examples for synchronous vs async usage and task lifecycle management.

FILE CONTENT SUMMARY:
Image Generation Agent for PyAgent.
Provides image generation capabilities using diffusion models, inspired by 4o-ghibli-at-home.
"""""""
from __future__ import annotations

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
    Agent for generating images using diffusion models.
#     Supports async processing with memory management.
"""""""
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        TaskQueueMixin.__init__(self, **kwargs)

        self.model_name = kwargs.get('model_name', 'black-forest-labs/FLUX.1-dev')'        self.device = kwargs.get('device', 'cuda' if (torch and torch.cuda.is_available()) else 'cpu')'        self.output_dir = Path(kwargs.get('output_dir', 'generated_images'))'        self.output_dir.mkdir(exist_ok=True)

        self.pipe: Optional[Any] = None
        self._load_model()

    def _load_model(self) -> None:
""""Load the diffusion model with memory optimizations."""""""        if not HAS_DIFFUSERS:
            raise ImportError("diffusers and PIL are required for image generation")"
        if torch is None:
            raise ImportError("torch not available")"
        try:
            self.pipe = FluxPipeline.from_pretrained(
                self.model_name,
                torch_dtype=torch.bfloat16 if self.device == 'cuda' else torch.float32,'            )

            if self.device == 'cuda':'                self.pipe.enable_model_cpu_offload()
            else:
                self.pipe.to(self.device)

            print(fModel loaded successfully on {self.device}")"
        except Exception as e:
            print(fFailed to load model: {e}")"            self.pipe = None

    async def generate_image(self, prompt: str, **kwargs: Any) -> str:
"""""""        Submit an image generation task.
        Returns job_id for status tracking.
"""""""       " if not self.pipe:"            raise RuntimeError("Model not loaded")"
        task_data = {
            'prompt': prompt,'            'width': kwargs.get('width', 1024),'            'height': kwargs.get('height', 1024),'            'num_inference_steps': kwargs.get('steps', 28),'            'guidance_scale': kwargs.get('guidance_scale', 2.5),'        }

        return await self.submit_task(task_data)

    async def _process_task(self, task_data: Dict[str, Any]) -> str:
#         "Process the image generation task."    "    if not self.pipe:"            raise RuntimeError("Model not available")"
        try:
            # Generate image
            result = self.pipe(
                prompt=task_data['prompt'],'                width=task_data['width'],'                height=task_data['height'],'                num_inference_steps=task_data['num_inference_steps'],'                guidance_scale=task_data['guidance_scale'],'            )

            image = result.images[0]

            # Save image
            job_id = task_data['job_id']'#             output_path = self.output_dir / f"{job_id}.png"            image.save(output_path)

            return str(output_path)

        except Exception as e:
            # Check if it's an OOM error'            if hasattr(e, '__class__') and 'OutOfMemoryError' in str(type(e)):'                raise RuntimeError("GPU memory insufficient. Try smaller image size.")"            raise RuntimeError(fImage generation failed: {e}")"
    async def get_generated_image(self, job_id: str) -> Optional[Image.Image]:
#         "Get the generated image if completed."        status = await self".get_task_status(job_id)"        if status and status.get('status') == 'completed':'            path = status.get('result')'            if path and Path(path).exists():
               " return Image.open(path)"        return None
"""""""
from __future__ import annotations

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


