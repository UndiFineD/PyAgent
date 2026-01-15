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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
# PyAgent Versioning Gatekeeper
# This file serves as the source of truth for the project's current maturity level.

from __future__ import annotations
from typing import Any

VERSION = "2.1.8-stable"
EVOLUTION_PHASE = 119
STABILITY_SCORE = 1.0  # Phase 108: Multi-Agent Logic Harvesting and Rust-Readiness verified



def is_gate_open(required_phase: int) -> bool:
    """Gatekeeping: Returns True if the system maturity allows for the required phase."""
    return EVOLUTION_PHASE >= required_phase




def get_version_info() -> dict[str, Any]:
    """Returns detailed version and phase information for orchestrators."""
    return {
        "version": VERSION,
        "phase": EVOLUTION_PHASE,
        "stability": STABILITY_SCORE,
        "rust_readiness": "Protocol typing > 80%, LogicCore isolation complete"
    }
