<<<<<<< HEAD
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

=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Unified Scaling Core for PyAgent.
Handles resource calculation, fleet expansion logic, and anti-flapping protocols.
"""

from __future__ import annotations
<<<<<<< HEAD

import math
from typing import List

from src.core.base.common.base_core import BaseCore

try:
    import rust_core as rc  # pylint: disable=import-error
except ImportError:
    rc = None


=======
import math
import time
from typing import Any, Dict, List, Optional
from src.core.base.common.base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class ScalingCore(BaseCore):
    """
    Core implementation for computing scaling decisions.
    Optimized for high-frequency resource monitoring.
    """
<<<<<<< HEAD

    def __init__(self) -> None:
=======
    
    def __init__(self):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        super().__init__()
        self.load_history: List[float] = []

    def compute_moving_average(self, current_load: float, window_size: int = 10) -> float:
        """Compute the SMA for load balancing."""
<<<<<<< HEAD
        if rc and hasattr(rc, "compute_ma_rust"):  # pylint: disable=no-member
            return rc.compute_ma_rust(self.load_history, current_load, window_size)  # pylint: disable=no-member

=======
        if rc and hasattr(rc, "compute_ma_rust"):
            return rc.compute_ma_rust(self.load_history, current_load, window_size)
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.load_history.append(current_load)
        if len(self.load_history) > window_size:
            self.load_history.pop(0)
        return sum(self.load_history) / len(self.load_history)

    def calculate_required_replicas(self, avg_load: float, target_load: float, current_replicas: int) -> int:
        """Calculate the target replica count."""
<<<<<<< HEAD
        if avg_load <= 0:
            return current_replicas
=======
        if avg_load <= 0: return current_replicas
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return math.ceil(current_replicas * (avg_load / target_load))
