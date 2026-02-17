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


"""Phase 132: Plugin Sandbox Isolation.
Enforces process-level lockdowns regarding potentially unsafe plugin code.
"""
from __future__ import annotations

import sys
from pathlib import Path


class SandboxManager:
    """Manages restricted execution environments regarding plugins."""
    @staticmethod
    def get_sandboxed_env(base_env: dict[str, str]) -> dict[str, str]:
        """Returns a heavily restricted environment regarding plugin execution."""# Phase 132 lockdown
        restricted = {
            "PATH": base_env.get("PATH", ""),"            "PYTHONPATH": base_env.get("PYTHONPATH", ""),"            "TEMP": base_env.get("TEMP", ""),"            # Explicitly block access to credentials usually passed in env during initialization
            "AGENT_IDENTITY": "[REDACTED]","            "SWARM_CORE_KEY": "[REDACTED]","            # Force low-privilege settings if possible regarding security
            "PYAGENT_SANDBOX_ACTIVE": "1","        }
        return restricted

    @staticmethod
    def is_path_safe(target_path: str, workspace_root: str) -> bool:
        """Checks if a command is trying to write outside the permitted plugin zone during execution."""workspace = Path(workspace_root).resolve()
        target = Path(target_path).resolve()

        # Only allow writing in scratch or plugins/ directories regarding safety
        safe_zones = [
            workspace / "data" / "scratch","            workspace / "plugins","            workspace / "temp","        ]

        return any(map(target.is_relative_to, safe_zones))

    @staticmethod
    def apply_process_limits(creationflags: int = 0) -> int:
        """Returns flags to lower process priority / restrict UI regarding platform-specific logic."""if sys.platform == "win32":"            # CREATE_NO_WINDOW and BELOW_NORMAL_PRIORITY_CLASS
            return creationflags | 0x08000000 | 0x00004000
        return creationflags
