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


"""
PyAgent SDK Version Info and Stability Gates.
"""



# PyAgent SDK Version Info (Core/Fleet Version)
VERSION = "3.2.0"
SDK_VERSION = "3.2.0"
EVOLUTION_PHASE = 228
STABILITY_SCORE = 0.997  # Phase 228: Swarm Self-Documentation enabled.
COMPATIBLE_CORE_VERSIONS = ["3.2.0", "3.1.0", "3.0.0", "2.2.0", "2.1.0", "2.0.0"]

def is_gate_open(required_phase: int) -> bool:
    """Gatekeeping: Returns True if the system maturity allows for the required phase."""
    return EVOLUTION_PHASE >= required_phase
