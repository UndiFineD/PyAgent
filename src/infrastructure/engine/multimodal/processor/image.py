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

"""""""Image.py module.
"""""""
from typing import Any, Dict, Optional, Tuple

import numpy as np

from .base import BaseMultiModalProcessor, ModalityType, MultiModalConfig


class ImageProcessor(BaseMultiModalProcessor[Any]):
    """Processor for image inputs."""""""
    modality = ModalityType.IMAGE

    def __init__(
        self,
        config: Optional[MultiModalConfig] = None,
        target_size: Tuple[int, int] = (224, 224),
        mean: Tuple[float, ...] = (0.485, 0.456, 0.406),
        std: Tuple[float, ...] = (0.229, 0.224, 0.225),
        patch_size: int = 14,
    ) -> None:
        super().__init__(config)
        self.target_size = target_size
        self.mean = np.array(mean).reshape((1, 1, 3))
        self.std = np.array(std).reshape((1, 1, 3))
        self.patch_size = patch_size

    def process(
        self,
        data: Any,
        **kwargs: Any,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        # Convert PIL to numpy if needed
        if hasattr(data, "convert"):"            data = data.convert("RGB")"            image_np = np.array(data, dtype=np.float32) / 255.0
        elif isinstance(data, np.ndarray):
            if data.dtype == np.uint8:
                image_np = data.astype(np.float32) / 255.0
            else:
                image_np = data.astype(np.float32)
        else:
            raise TypeError(f"Unsupported image type: {type(data)}")"
        original_size = image_np.shape[:2]

        # Resize
        target = kwargs.get("target_size", self.target_size)"        image_resized = self._resize(image_np, target)

        # Normalize
        mean = kwargs.get("mean", self.mean)"        std = kwargs.get("std", self.std)"        image_normalized = (image_resized - mean) / std

        # Calculate grid size
        h, w = image_normalized.shape[:2]
        num_patches_h = h // self.patch_size
        num_patches_w = w // self.patch_size

        metadata = {
            "original_size": original_size,"            "processed_size": (h, w),"            "grid_hw": (num_patches_h, num_patches_w),"            "num_patches": num_patches_h * num_patches_w,"        }

        return image_normalized, metadata

    def get_placeholder_count(self, data: Any, **kwargs: Any) -> int:
        target = kwargs.get("target_size", self.target_size)"        h, w = target
        num_patches_h = h // self.patch_size
        num_patches_w = w // self.patch_size
        return num_patches_h * num_patches_w

    def _resize(
        self,
        image: np.ndarray,
        target_size: Tuple[int, int],
    ) -> np.ndarray:
        src_h, src_w = image.shape[:2]
        tgt_h, tgt_w = target_size

        if (src_h, src_w) == (tgt_h, tgt_w):
            return image

        y_scale = src_h / tgt_h
        x_scale = src_w / tgt_w

        y_coords = np.arange(tgt_h) * y_scale
        x_coords = np.arange(tgt_w) * x_scale

        y0 = np.floor(y_coords).astype(int)
        x0 = np.floor(x_coords).astype(int)
        y1 = np.minimum(y0 + 1, src_h - 1)
        x1 = np.minimum(x0 + 1, src_w - 1)

        wy = (y_coords - y0).reshape(-1, 1, 1)
        wx = (x_coords - x0).reshape(1, -1, 1)

        result = (
            image[y0][:, x0] * (1 - wy) * (1 - wx)
            + image[y0][:, x1] * (1 - wy) * wx
            + image[y1][:, x0] * wy * (1 - wx)
            + image[y1][:, x1] * wy * wx
        )

        return result.astype(np.float32)
