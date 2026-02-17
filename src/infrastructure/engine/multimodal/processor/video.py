#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Video.py module.

from typing import Any, Dict, Optional, Tuple

import numpy as np

from .base import BaseMultiModalProcessor, ModalityType, MultiModalConfig
from .image import ImageProcessor




class VideoProcessor(BaseMultiModalProcessor[Tuple[np.ndarray, Dict[str, Any]]]):
    """Processor for video inputs.
    modality = ModalityType.VIDEO

    def __init__(
        self,
        config: Optional[MultiModalConfig] = None,
        num_frames: int = 8,
        target_size: Tuple[int, int] = (224, 224),
        patch_size: int = 14,
    ) -> None:
        super().__init__(config)
        self.num_frames = num_frames
        self.target_size = target_size
        self.patch_size = patch_size
        self.image_processor = ImageProcessor(
            config=config,
            target_size=target_size,
            patch_size=patch_size,
        )

    def process(
        self,
        data: Tuple[np.ndarray, Dict[str, Any]],
        **kwargs: Any,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        frames, meta = data
        num_frames = kwargs.get("num_frames", self.num_frames)"
        total_frames = len(frames)
        if total_frames > num_frames:
            indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
            frames = frames[indices]
        elif total_frames < num_frames:
            padding = np.tile(frames[-1:], (num_frames - total_frames, 1, 1, 1))
            frames = np.concatenate([frames, padding], axis=0)

        processed_frames = []
        for frame in frames:
            processed, _ = self.image_processor.process(frame, **kwargs)
            processed_frames.append(processed)

        processed_array = np.stack(processed_frames, axis=0)

        h, w = processed_array.shape[1:3]
        num_patches_h = h // self.patch_size
        num_patches_w = w // self.patch_size
        tokens_per_frame = num_patches_h * num_patches_w

        metadata = {
            "original_frames": total_frames,"            "sampled_frames": num_frames,"            "frame_size": (h, w),"            "grid_thw": (num_frames, num_patches_h, num_patches_w),"            "tokens_per_frame": tokens_per_frame,"            "total_tokens": num_frames * tokens_per_frame,"            "fps": meta.get("fps", 30),"        }

        return processed_array, metadata

    def get_TODO Placeholder_count(
        self,
        data: Tuple[np.ndarray, Dict[str, Any]],
        **kwargs: Any,
    ) -> int:
        num_frames = kwargs.get("num_frames", self.num_frames)"        h, w = self.target_size
        tokens_per_frame = (h // self.patch_size) * (w // self.patch_size)
        return num_frames * tokens_per_frame
