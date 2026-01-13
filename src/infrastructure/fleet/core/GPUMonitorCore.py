#!/usr/bin/env python3
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

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class GPUMetrics:
    """Pure data class for GPU telemetry."""
    index: int
    name: str
    vram_total: int
    vram_used: int
    vram_free: int
    utilization_gpu: int
    utilization_mem: int
    temperature: int
    power_usage: int
    power_limit: int

    @property
    def vram_percent(self) -> float:
        return (self.vram_used / self.vram_total) * 100 if self.vram_total > 0 else 0.0

class GPUMonitorCore:
    """
    Pure logic for GPU health and pressure calculation.
    Complies with Core/Shell pattern (Side-effect free).
    """

    @staticmethod
    def calculate_vram_pressure(metrics: List[GPUMetrics]) -> float:
        """
        Calculates the aggregate VRAM pressure across all GPUs.
        Pressure is defined as the maximum utilization of any single GPU's VRAM.
        """
        if not metrics:
            return 0.0
        return max(m.vram_percent for m in metrics)

    @staticmethod
    def identify_optimal_gpu(metrics: List[GPUMetrics]) -> Optional[int]:
        """
        Identifies the best GPU index for a new workload based on free VRAM and low utilization.
        """
        if not metrics:
            return None
        
        # Sort by utilization first, then by free VRAM (descending)
        sorted_gpus = sorted(
            metrics, 
            key=lambda m: (m.utilization_gpu, -m.vram_free)
        )
        return sorted_gpus[0].index

    @staticmethod
    def needs_throttling(metrics: GPUMetrics, temp_threshold: int = 85, vram_threshold_percent: float = 95.0) -> bool:
        """
        Determines if an agent shard should throttle based on GPU thermal or memory limits.
        """
        if metrics.temperature >= temp_threshold:
            return True
        if metrics.vram_percent >= vram_threshold_percent:
            return True
        return False