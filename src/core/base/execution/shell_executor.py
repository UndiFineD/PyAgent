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
Shell execution core for agents.
Handles subprocess spawning, environment propagation, and interaction recording.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
from typing import Any

from src.core.base.common.shell_core import ShellCore
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ShellExecutor:
    """
    Safely executes shell commands and records outcomes.
    Standardized Facade over ShellCore (Phase 317).
    """

    _core: ShellCore | None = None

    @classmethod
    def _get_core(cls) -> ShellCore:
        if cls._core is None:
            cls._core = ShellCore()
        return cls._core

    @staticmethod
    async def async_run_command(  # pylint: disable=too-many-arguments, too-many-positional-arguments
        cmd: list[str],
        workspace_root: str,
        agent_name: str,
        models_config: Any | None = None,
        recorder: Any | None = None,
        timeout: int = 120,
    ) -> subprocess.CompletedProcess[str]:
        """Phase 266: Asynchronous subprocess execution via ShellCore."""
        _ = agent_name
        core = ShellExecutor._get_core()

        env = {}
        if models_config:
            env["AGENT_MODELS_CONFIG"] = json.dumps(models_config)

        # Use common core for execution
        result = await core.execute_async(cmd=cmd, timeout=timeout, env=env, cwd=workspace_root, sanitize=True)

        if recorder:
            recorder.record_interaction(
                provider="ShellAsync",
                model="async_subprocess",
                prompt=" ".join(cmd),
                result=result.stdout + result.stderr,
                meta={"exit_code": result.returncode},
            )

        return subprocess.CompletedProcess(
            args=cmd, returncode=result.returncode, stdout=result.stdout, stderr=result.stderr
        )

    @staticmethod
    def run_command(  # pylint: disable=too-many-arguments, too-many-positional-arguments
        cmd: list[str],
        workspace_root: str,
        agent_name: str,
        models_config: Any | None = None,
        recorder: Any | None = None,
        timeout: int = 120,
        max_retries: int = 1,
    ) -> subprocess.CompletedProcess[str]:
        """Run a command via core synchronous execution."""
        _ = agent_name
        # For simplicity, we can use ShellCore's execute_sync logic if we add it,
        # or just keep subprocess.run for now but ensure env parity.
        core = ShellExecutor._get_core()

        env = os.environ.copy()
        if models_config:
            env["AGENT_MODELS_CONFIG"] = json.dumps(models_config)

        env = core.sanitize_env(env)

        last_error = None
        for attempt in range(max_retries):
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env,
                    cwd=workspace_root,
                    check=False,
                )

                if recorder:
                    recorder.record_interaction(
                        provider="Shell",
                        model="subprocess",
                        prompt=" ".join(cmd),
                        result=result.stdout + result.stderr,
                        meta={"exit_code": result.returncode, "attempt": attempt + 1},
                    )

                return result
            except subprocess.TimeoutExpired as e:
                logging.warning("Timeout (attempt %s/%s)", attempt + 1, max_retries)
                last_error = e
            except Exception as e:  # pylint: disable=broad-exception-caught
                logging.error("Execution failure: %s", e)
                last_error = e

        if isinstance(last_error, subprocess.TimeoutExpired):
            raise last_error

        return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr=str(last_error))
