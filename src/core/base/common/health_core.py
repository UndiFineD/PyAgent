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

"""
Core logic for system health monitoring and diagnostics.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

from .base_core import BaseCore
from .models import AgentHealthCheck, HealthStatus

try:
    import rust_core as rc
except ImportError:
    rc = None


class HealthCore(BaseCore):
    """
    Authoritative engine for health checks across the swarm.
    """

    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        super().__init__()
        self.workspace_root = workspace_root or Path.cwd()
        self.results: Dict[str, AgentHealthCheck] = {}

    def check_git(self) -> AgentHealthCheck:
        """Check if git is installed and responsive."""
        start_time = time.time()
        try:
            result = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=5, check=False)
            ms = (time.time() - start_time) * 1000
            if result.returncode == 0:
                return AgentHealthCheck(
                    agent_name="git",
                    status=HealthStatus.HEALTHY,
                    response_time_ms=ms,
                    details={"version": result.stdout.strip()},
                )
        except (subprocess.SubprocessError, OSError) as e:
            return AgentHealthCheck(agent_name="git", status=HealthStatus.UNHEALTHY, error_message=str(e))
        return AgentHealthCheck(agent_name="git", status=HealthStatus.UNHEALTHY)

    def check_python(self) -> AgentHealthCheck:
        """Return details about the current Python environment."""
        return AgentHealthCheck(
            agent_name="python",
            status=HealthStatus.HEALTHY,
            response_time_ms=0,
            details={"version": sys.version, "executable": sys.executable},
        )

    def check_fleet_health(self, agent_heartbeats: Dict[str, float]) -> List[str]:
        """Detect stale agents using high-speed Rust core if available."""
        if rc and hasattr(rc, "detect_failed_agents_rust"):  # pylint: disable=no-member
            # pylint: disable=no-member
            return rc.detect_failed_agents_rust(agent_heartbeats, 30.0)

        # Fallback
        now = time.time()
        return [name for name, last_seen in agent_heartbeats.items() if (now - last_seen) > 30.0]

    def run_all(self) -> Dict[str, AgentHealthCheck]:
        """Execute all registers health checks."""
        self.results["python"] = self.check_python()
        self.results["git"] = self.check_git()
        return self.results
