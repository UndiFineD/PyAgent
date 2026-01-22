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
<<<<<<< HEAD
from typing import Any, Optional, Dict

from src.core.base.common.shell_core import ShellCore
from src.core.base.lifecycle.version import VERSION
=======
import logging
import asyncio
from typing import Any
from src.core.base.common.shell_core import ShellCore
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

__version__ = VERSION

class ShellExecutor:
    """
    Safely executes shell commands and records outcomes.
    Standardized Facade over ShellCore (Phase 317).
    """

<<<<<<< HEAD
    _core: Optional[ShellCore] = None
=======
class ShellExecutor:
    """
    Safely executes shell commands and records outcomes.
    Standardized Facade over ShellCore (Phase 317).
    """
    _core: ShellCore | None = None
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    @classmethod
    def _get_core(cls) -> ShellCore:
        if cls._core is None:
            cls._core = ShellCore()
        return cls._core

    @staticmethod
    async def async_run_command(
        cmd: list[str],
        workspace_root: str,
        agent_name: str,
        models_config: Optional[Any] = None,
        recorder: Optional[Any] = None,
        timeout: int = 120,
    ) -> subprocess.CompletedProcess[str]:
        """Phase 266: Asynchronous subprocess execution via ShellCore."""
<<<<<<< HEAD
        _ = agent_name
        core: ShellCore = ShellExecutor._get_core()

        env: Dict[str, str] = {}
        if models_config:
            env["AGENT_MODELS_CONFIG"] = json.dumps(models_config)

        result: subprocess.CompletedProcess = await core.execute_async(cmd=cmd, timeout=timeout, env=env, cwd=workspace_root, sanitize=True)

        if recorder:
            output = result.stdout + result.stderr
=======
        core = ShellExecutor._get_core()
        
        env = {}
        if models_config:
            import json
            env["AGENT_MODELS_CONFIG"] = json.dumps(models_config)

        # Use common core for execution
        result = await core.execute_async(
            cmd=cmd,
            timeout=timeout,
            env=env,
            cwd=workspace_root,
            sanitize=True
        )

        if recorder:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            recorder.record_interaction(
                provider="ShellAsync",
                model="async_subprocess",
                prompt=" ".join(cmd),
<<<<<<< HEAD
                result=output,
=======
                result=result.stdout + result.stderr,
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                meta={"exit_code": result.returncode},
            )

        return subprocess.CompletedProcess(
<<<<<<< HEAD
            args=cmd, returncode=result.returncode, stdout=result.stdout, stderr=result.stderr
=======
            args=cmd, 
            returncode=result.returncode, 
            stdout=result.stdout, 
            stderr=result.stderr
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        )

    @staticmethod
    def run_command(
        cmd: list[str],
        workspace_root: str,
        agent_name: str,
        models_config: Optional[Any] = None,
        recorder: Optional[Any] = None,
        timeout: int = 120,
        max_retries: int = 1,
    ) -> subprocess.CompletedProcess[str]:
        """Run a command via core synchronous execution."""
<<<<<<< HEAD
        _ = agent_name
        core: ShellCore = ShellExecutor._get_core()
=======
        # For simplicity, we can use ShellCore's execute_sync logic if we add it, 
        # or just keep subprocess.run for now but ensure env parity.
        core = ShellExecutor._get_core()
        
        env = os.environ.copy()
        if models_config:
            import json
            env["AGENT_MODELS_CONFIG"] = json.dumps(models_config)
        
        env = core.sanitize_env(env)
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

        env: Dict[str, str] = os.environ.copy()
        if models_config:
            env["AGENT_MODELS_CONFIG"] = json.dumps(models_config)

        env = core.sanitize_env(env)

        last_error: Optional[Exception] = None
        for attempt in range(max_retries):
            try:
<<<<<<< HEAD
                result: subprocess.CompletedProcess = subprocess.run(
=======
                result = subprocess.run(
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
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
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logging.error("Execution failure: %s", e)
                last_error = e

        if isinstance(last_error, subprocess.TimeoutExpired):
            raise last_error
<<<<<<< HEAD

        return subprocess.CompletedProcess(args=cmd, returncode=1, stdout="", stderr=str(last_error))
=======
        
        return subprocess.CompletedProcess(
            args=cmd, returncode=1, stdout="", stderr=str(last_error)
        )
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
