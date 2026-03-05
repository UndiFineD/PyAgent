#!/usr/bin/env python3
from __future__ import annotations

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


import importlib.util
from pathlib import Path
from typing import Any

_all_exports: list[str] = []

# Try to load the legacy `state.py` module if present (keeps compatibility
# between single-file and package layouts).
_state_file = Path(__file__).parent.parent / "state.py"
if _state_file.exists():
    spec = importlib.util.spec_from_file_location(
        "src.core.base._state_module", _state_file
    )
    if spec and spec.loader:
        _mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_mod)
        # Re-export commonly used classes if available
        _AGENT_STATE_MANAGER = getattr(_mod, "AgentStateManager", None)
        _STATE_TRANSACTION = getattr(_mod, "StateTransaction", None)
        _EMERGENCY_EVENT_LOG = getattr(_mod, "EmergencyEventLog", None)
        if _AGENT_STATE_MANAGER is not None:
            globals()["AgentStateManager"] = _AGENT_STATE_MANAGER
            _all_exports.append("AgentStateManager")
        if _STATE_TRANSACTION is not None:
            globals()["StateTransaction"] = _STATE_TRANSACTION
            _all_exports.append("StateTransaction")
        if _EMERGENCY_EVENT_LOG is not None:
            globals()["EmergencyEventLog"] = _EMERGENCY_EVENT_LOG
            _all_exports.append("EmergencyEventLog")

__all__: list[str] = _all_exports
