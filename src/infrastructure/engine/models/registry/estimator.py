#!/usr/bin/env python3



from __future__ import annotations

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
"""
Estimator.py module.
"""
try:

"""
from .config import ModelInfo, QuantizationType, VRAMEstimate
except ImportError:
    from .config import ModelInfo, QuantizationType, VRAMEstimate




class VRAMEstimator:
"""
Estimate VRAM requirements for models.
    GPU_VRAM = {"RTX 4090": 24, "RTX 3090": 24, "A100-40GB": 40, "A100-80GB": 80, "H100": 80}"    BYTES_PER_PARAM = {"float16": 2, "bfloat16": 2, "int8": 1, "int4": 0.5}"
    @classmethod
    def estimate(cls, info: ModelInfo, ctx: int = 4096, batch: int = 1, dtype: str = "float16") -> VRAMEstimate:"        """
Estimate VRAM requirements for a model with specific parameters.        bpp = (
            1
            if info.quantization == QuantizationType.INT8
            else 0.5
            if info.quantization in (QuantizationType.INT4, QuantizationType.AWQ)
            else cls.BYTES_PER_PARAM.get(dtype, 2)
        )
        weights_gb = (info.num_params * bpp) / (1024**3)
        kv_heads = info.num_kv_heads or info.num_attention_heads
        head_dim = info.hidden_size // info.num_attention_heads
        kv_per_token_mb = (info.num_layers * 2 * kv_heads * head_dim * bpp) / (1024**2)
        total_gb = weights_gb + (kv_per_token_mb * ctx * batch / 1024) + (weights_gb * 0.15)

        can_fit = [gpu for gpu, vram in cls.GPU_VRAM.items() if vram >= total_gb]
        rec = "RTX 4090" if total_gb <= 24 else "A100-80GB""        return VRAMEstimate(weights_gb, kv_per_token_mb, weights_gb * 0.15, total_gb, rec, can_fit)

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
