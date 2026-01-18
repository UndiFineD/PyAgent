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
from src.core.base.Version import VERSION
import os
import subprocess
import logging
import asyncio
from typing import Any

__version__ = VERSION


class EnvironmentSanitizer:
    """Filters environment variables to prevent secret leakage (Phase 266)."""

    ALLOW_LIST = {
        "PATH",
        "PYTHONPATH",
        "LANG",
        "LC_ALL",
        "LC_CTYPE",
        "SYSTEMROOT",
        "WINDIR",
        "USERPROFILE",
        "HOME",
        "TEMP",
        "TMP",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "NO_PROXY",
        "DV_AGENT_PARENT",
        "AGENT_MODELS_CONFIG",
    }

    @classmethod
    def sanitize(cls, env: dict[str, str]) -> dict[str, str]:
        """Returns a copy of the environment containing only allow-listed variables."""
        return {k: v for k, v in env.items() if k.upper() in cls.ALLOW_LIST}


class ShellExecutor:
    """Safely executes shell commands and records outcomes."""

    @staticmethod
    async def async_run_command(
        cmd: list[str],
        workspace_root: str,
        agent_name: str,
        models_config: Any | None = None,
        recorder: Any | None = None,
        timeout: int = 120,
    ) -> subprocess.CompletedProcess[str]:
        """Phase 266: Asynchronous subprocess execution with real-time streaming."""
        logging.debug(
            f"Async-Running command: {' '.join(cmd[:3])}... (timeout={timeout}s)"
        )

        env = os.environ.copy()
        if models_config:
            import json

            env["AGENT_MODELS_CONFIG"] = json.dumps(models_config)

        env = EnvironmentSanitizer.sanitize(env)

        # Phase 132: Apply Sandbox if running in plugin directory
        from src.core.base.SandboxManager import SandboxManager

        if "plugins" in workspace_root or any("plugins" in c for c in cmd):
            logging.info(f"ShellExecutor: Activating Sandbox Lockdown for {agent_name}")
            env = SandboxManager.get_sandboxed_env(env)

        try:
            # Phase 266/132: Start async subprocess with potential flags
            creationflags = (
                SandboxManager.apply_process_limits() if os.name == "nt" else 0
            )

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
                cwd=workspace_root,
                creationflags=creationflags,
            )

            stdout_data: list[Any] = []
            stderr_data: list[Any] = []

            async def stream_reader(
                pipe: asyncio.StreamReader, container: list[str], label: str
            ) -> None:
                while True:
                    line = await pipe.readline()
                    if not line:
                        break
                    line_str = line.decode("utf-8", errors="replace").rstrip()
                    container.append(line_str)
                    # Real-time streaming to StructuredLogger (simulated via logging)
                    logging.debug(f"[{agent_name}][{label}] {line_str}")

            # Read stdout and stderr concurrently
            try:
                await asyncio.wait_for(
                    asyncio.gather(
                        stream_reader(process.stdout, stdout_data, "STDOUT"),
                        stream_reader(process.stderr, stderr_data, "STDERR"),
                    ),
                    timeout=timeout,
                )
            except asyncio.TimeoutExpired:  # type: ignore[attr-defined]
                process.kill()
                logging.error(
                    f"Async shell command TIMEOUT after {timeout}s: {' '.join(cmd)}"
                )
                raise

            returncode = await process.wait()
            full_stdout = "\n".join(stdout_data)
            full_stderr = "\n".join(stderr_data)

            if recorder:
                recorder.record_interaction(
                    provider="ShellAsync",
                    model="async_subprocess",
                    prompt=" ".join(cmd),
                    result=full_stdout + full_stderr,
                    meta={"exit_code": returncode},
                )

            return subprocess.CompletedProcess(
                args=cmd, returncode=returncode, stdout=full_stdout, stderr=full_stderr
            )

        except Exception as e:
            logging.error(f"Async execution failure: {e}")
            return subprocess.CompletedProcess(
                args=cmd, returncode=1, stdout="", stderr=str(e)
            )

    @staticmethod
    def run_command(
        cmd: list[str],
        workspace_root: str,
        agent_name: str,
        models_config: Any | None = None,
        recorder: Any | None = None,
        timeout: int = 120,
        max_retries: int = 1,
    ) -> subprocess.CompletedProcess[str]:
        """Run a command with full environment and telemetry support."""
        logging.debug(f"Running command: {' '.join(cmd[:3])}... (timeout={timeout}s)")

        last_error = None
        for attempt in range(max_retries):
            try:
                env = os.environ.copy()

                # Model and Parent propagation
                if os.environ.get("DV_AGENT_PARENT"):
                    env["DV_AGENT_PARENT"] = os.environ.get("DV_AGENT_PARENT")

                if models_config:
                    import json

                    env["AGENT_MODELS_CONFIG"] = json.dumps(models_config)

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env,
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
                logging.warning(f"Timeout (attempt {attempt + 1}/{max_retries})")
                last_error = e
            except Exception as e:
                logging.error(f"Execution failure: {e}")
                last_error = e

        if isinstance(last_error, subprocess.TimeoutExpired):
            raise last_error
        return subprocess.CompletedProcess(
            " ".join(cmd), 1, stdout="", stderr=str(last_error)
        )
