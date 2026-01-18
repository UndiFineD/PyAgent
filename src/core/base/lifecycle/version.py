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
PyAgent SDK Version Info and Stability Gates.
"""

from __future__ import annotations

# PyAgent SDK Version Info (Core/Fleet Version)
VERSION = "3.7.0"
SDK_VERSION = "3.7.0"
EVOLUTION_PHASE = 318
STABILITY_SCORE = 1.000
GOLDEN_MASTER_SEAL = True
COMPATIBLE_CORE_VERSIONS = [
    "3.6.0",
    "3.5.1",
    "3.5.0",
    "3.4.0",
    "3.3.0",
    "3.2.0",
    "3.1.0",
    "3.0.0",
    "2.2.0",
]


def is_gate_open(required_phase: int) -> bool:
    """Gatekeeping: Returns True if the system maturity allows for the required phase."""
    return EVOLUTION_PHASE >= required_phase
