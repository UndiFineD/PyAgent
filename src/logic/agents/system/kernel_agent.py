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


"""Agent specializing in OS-level operations, environment management, and system diagnosis.
Inspired by Open Interpreter and Openator.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import platform
import shutil
import sys

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.security.security_guard_agent import SecurityGuardAgent

__version__ = VERSION


class KernelAgent(BaseAgent):
    """Interacts directly with the host OS to manage environments and perform diagnostics."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.security_guard = SecurityGuardAgent(file_path + ".audit")
        self._system_prompt = (
            "You are the Kernel Agent. "
            "Your role is to manage the host environment and perform system-level tasks. "
            "You can check system resources, manage files, and execute shell commands. "
            "Always prioritize safety and verify commands before execution."
        )

    @as_tool
    async def get_system_info(self) -> str:
        """Returns details about the current operating system and environment."""

        def get_info() -> str:
            info = {
                "os": platform.system(),
                "version": platform.version(),
                "machine": platform.machine(),
                "python_version": sys.version,
                "cwd": os.getcwd(),
                "env_vars": list(os.environ.keys())[:10],  # First 10 for brevity
            }
            return json.dumps(info, indent=2)

        return await asyncio.to_thread(get_info)

    @as_tool
    async def check_disk_space(self, path: str = ".") -> str:
        """Checks available disk space at the specified path."""
        try:
            total, used, free = await asyncio.to_thread(shutil.disk_usage, path)
            return (
                f"Disk Usage for {path}: {used // (2**30)}GB used / "
                f"{free // (2**30)}GB free (Total: {total // (2**30)}GB)"
            )
        except Exception as e:
            return f"Error checking disk space: {e}"

    @as_tool
    async def execute_shell(self, command: str, force: bool = False) -> str:
        """Executes a shell command and returns the output (STDOUT + STDERR).
        High-risk commands require 'force=True' as a HITL gate.
        """
        logging.warning(f"KernelAgent auditing shell command: {command}")

        # Security Audit (HITL Gate)
        risk_level, warning = await asyncio.to_thread(self.security_guard.audit_command, command)
        if risk_level == "HIGH" and not force:
            return (
                f"BLOCKED: High-risk command detected.\n"
                f"Warning: {warning}\n"
                f"To execute this command, you must explicitly set 'force=True' as a Human-in-the-loop verification."
            )

        try:
            # Phase 287: Use asyncio for sub-processes
            proc = await asyncio.create_subprocess_shell(
                command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
                output = f"STDOUT:\n{stdout.decode()}\n"
                if stderr:
                    output += f"STDERR:\n{stderr.decode()}\n"

                # Intelligence Harvesting (Phase 108)
                if hasattr(self, "recorder") and self.recorder:
                    self.recorder.record_lesson(
                        "kernel_shell_exec",
                        {"command": command, "exit_code": proc.returncode},
                    )

                return output
            except asyncio.TimeoutExpired:  # type: ignore[attr-defined]
                proc.kill()
                await proc.wait()
                if hasattr(self, "recorder") and self.recorder:
                    self.recorder.record_lesson("kernel_shell_timeout", {"command": command})
                return "Error: Command timed out after 30 seconds."

        except Exception as e:
            if hasattr(self, "recorder") and self.recorder:
                self.recorder.record_lesson("kernel_shell_error", {"command": command, "error": str(e)})
            return f"Error executing command: {e}"
