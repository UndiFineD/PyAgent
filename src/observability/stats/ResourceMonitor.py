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

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Engine for monitoring system resources (CPU, Memory, Disk)."""



import os
import logging
import platform
import json
from pathlib import Path
from typing import Dict, Any, Optional



































try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

class ResourceMonitor:
    """Monitors local system load to inform agent execution strategies."""
    
    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.stats_file = self.workspace_root / ".system_stats.json"

    def get_current_stats(self) -> Dict[str, Any]:
        """Collects current CPU, Memory, and Disk metrics."""
        stats = {
            "platform": platform.platform(),
            "cpu_usage_pct": 0,
            "memory_usage_pct": 0,
            "disk_free_gb": 0,
            "status": "UNAVAILABLE",
            "gpu": {"available": False, "type": "NONE"}
        }
        
        if not HAS_PSUTIL:
            return stats
            
        try:
            stats["cpu_usage_pct"] = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            stats["memory_usage_pct"] = mem.percent
            
            disk = psutil.disk_usage(str(self.workspace_root))
            stats["disk_free_gb"] = round(disk.free / (1024**3), 2)
            
            # GPU Detection (Hardware-Aware Orchestration - Phase 126)
            stats["gpu"] = self._detect_gpu()
            
            # Simple threshold logic
            if stats["cpu_usage_pct"] > 90 or stats["memory_usage_pct"] > 90:
                stats["status"] = "CRITICAL"
            elif stats["cpu_usage_pct"] > 70 or stats["memory_usage_pct"] > 70:
                stats["status"] = "WARNING"
            else:
                stats["status"] = "HEALTHY"
                
        except Exception as e:
            logging.error(f"Failed to gather resource stats: {e}")
            stats["status"] = "ERROR"
            
        return stats

    def _detect_gpu(self) -> Dict[str, Any]:
        """Detects if NVIDIA or AMD GPUs are available."""
        # Check for NVIDIA (via nvidia-smi if available)
        import shutil
        if shutil.which("nvidia-smi"):
            return {"available": True, "type": "NVIDIA"}
        
        # Fallback to checking for torch/tensorflow availability if installed
        try:
            import torch
            if torch.cuda.is_available():
                return {"available": True, "type": "NVIDIA (Torch)"}
        except ImportError:
            pass
            
        return {"available": False, "type": "NONE"}

    def save_stats(self) -> str:
        """Saves current stats to disk."""
        stats = self.get_current_stats()
        try:
            self.stats_file.write_text(json.dumps(stats, indent=2))
        except Exception as e:
            logging.error(f"Failed to save system stats: {e}")

    def get_market_multiplier(self) -> float:
        """Determines the surcharge multiplier based on load."""
        stats = self.get_current_stats()
        multiplier = 1.0
        
        if stats["status"] == "CRITICAL":
            multiplier = 3.0
        elif stats["status"] == "WARNING":
            multiplier = 1.5
            
        if stats.get("gpu", {}).get("available"):
            multiplier += 1.0 # Additive premium for GPU availability
            
        return multiplier

    def get_execution_recommendation(self) -> str:
        """Suggests whether to run heavy tasks."""
        stats = self.get_current_stats()
        if stats["status"] == "CRITICAL":
            return "PAUSE: System load is too high. Defer heavy indexing or LLM calls."
        elif stats["status"] == "WARNING":
            return "CAUTION: Elevated load. Run tasks sequentially rather than in parallel."
        return "PROCEED: System resources are sufficient."

if __name__ == "__main__":
    mon = ResourceMonitor("c:/DEV/PyAgent")
    print(json.dumps(mon.get_current_stats(), indent=2))
    print(f"Recommendation: {mon.get_execution_recommendation()}")
