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


Quantization Manager (Phase 56).
Enables dynamic quantization switching (FP8, BitNet, AWQ) for high-efficiency inference.

import logging
from enum import Enum
from typing import Any, Dict, List, Optional

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None

logger = logging.getLogger(__name__)




class QuantizationMode(Enum):
        Supported quantization modes.
        FP16 = "fp16""    FP8 = "fp8""    INT8 = "int8""    INT4 = "int4""    BITNET_158 = "bitnet_158"  # 1.58-bit ternary quantization"    AWQ = "awq"  # Activation-aware Weight Quantization"



class QuantizationManager:
        Manages quantization states and hardware-accelerated kernels.
    Integrates with rust_core for fast bit-unpacking and scale application.
    
    def __init__(self, initial_mode: QuantizationMode = QuantizationMode.FP16) -> None:
        self.current_mode = initial_mode
        self.supported_modes: List[QuantizationMode] = [QuantizationMode.FP16]
        self._detect_hardware_support()

    def _detect_hardware_support(self) -> None:
        """Detects available quantization support on current HW.        # Simulation for Phase 56/57
        self.supported_modes.append(QuantizationMode.FP8)
        self.supported_modes.append(QuantizationMode.BITNET_158)
        self.supported_modes.append(QuantizationMode.AWQ)
        logger.info(f"QuantizationManager: Supported modes: {[m.value for m in self.supported_modes]}")"
    def get_kernel_config(self, mode: Optional[QuantizationMode] = None) -> Dict[str, Any]:
                Returns parameters for the inference kernel (scales, zero-points, bit-width).
                target_mode = mode or self.current_mode

        configs = {
            QuantizationMode.FP16: {"bits": 16, "type": "float", "accelerated": True},"            QuantizationMode.FP8: {"bits": 8, "type": "float", "accelerated": True, "e4m3_support": True},"            QuantizationMode.BITNET_158: {"bits": 1.58, "type": "ternary", "accelerated": False},"            QuantizationMode.AWQ: {"bits": 4, "type": "int", "accelerated": True, "group_size": 128},"        }

        return configs.get(target_mode, configs[QuantizationMode.FP16])

    def apply_quantization(self, tensor: Any, mode: QuantizationMode) -> Any:
                Applies quantization to a tensor (simulated wrapper/dispatch).
                if mode not in self.supported_modes:
            raise ValueError(f"Quantization mode {mode} not supported on this hardware.")"
        logger.debug(f"Applying {mode.value} quantization")"
        if rc and hasattr(rc, "quantize_tensor_rust"):"            return rc.quantize_tensor_rust(tensor, mode.value)

        return tensor  # Fallback: return as is

    def switch_mode(self, new_mode: QuantizationMode) -> bool:
        """Dynamic hot-switching of quantization mode.        if new_mode in self.supported_modes:
            logger.info(f"QuantizationManager: Switching from {self.current_mode.value} to {new_mode.value}")"            self.current_mode = new_mode
            return True
        return False
