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


"""
"""
Unified shell execution core for all PyAgent services.""

"""
import asyncio
import logging
import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union

try:
    import rust_core as rc  # pylint: disable=import-error
except ImportError:
    rc = None


@dataclass(frozen=True)
class ShellResult:
"""
The result of a shell command execution.""
command: List[str]
    returncode: int
    stdout: str
    stderr: str
    duration: float
    success: bool = field(init=False)

    def __post_init__(self) -> None:
        # success is True if returncode is 0
        object.__setattr__(self, "success", self.returncode == 0)


    def __str__(self) -> str:
        return f"ShellResult(rc={self.returncode}, success={self.success}, duration={self.duration:.2f}s)"



class ShellCore:
"""
Centralized handler for shell and subprocess operations.
    Provides consistent logging, error handling, and environmental setup.
"""
def __init__(self, repo_root: Optional[Union[str, Path]] = None) -> None:
        if repo_root:
            self.repo_root = Path(repo_root)
        else:
            try:
                from ..configuration.config_manager import \
                    CoreConfigManager  # pylint: disable=import-outside-toplevel

                # CoreConfigManager inherits from BaseCore which provides repo_root
                config = CoreConfigManager()
                self.repo_root = getattr(config, "repo_root", Path.cwd())
            except (ImportError, Exception):  # pylint: disable=unused-variable, broad-exception-caught
                self.repo_root = Path.cwd()

        self.logger = logging.getLogger("pyagent.shell")
        self._ansi_escape = re.compile(r"\x1B(?:[@-Z\-_]|\[[0-?]*[ -/]*[@-~])")


    def sanitize_env(self, env: Dict[str, str]) -> Dict[str, str]:
"""
Filters environment variables to prevent secret leakage.

        This is intentionally conservative; prefer allowing well-known environment
        variables and the `PYAGENT_` / `DV_` prefixes.
"""
allow_list = {
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
            "AGENT_MODELS_CONFIG",
            "PYAGENT_ENV",
            "AGENT_NAME",
            "WORKSPACE_ROOT",
        }
        sanitized: Dict[str, str] = {}
        for k, v in env.items():
            k_upper = k.upper()
            if k_upper in allow_list or k_upper.startswith("PYAGENT_") or k_upper.startswith("DV_"):
                sanitized[k] = v
        return sanitized


    def strip_ansi(self, text: str) -> str:
"""
Removes ANSI escape sequences from a string.

        Safe for None/empty input.
"""
if not text:
            return ""
        return self._ansi_escape.sub("", text)


    def _record_shell_interaction(self, provider: str, prompt: str, result_text: str, meta: Dict[str, object]) -> None:
"""
Helper to record shell interactions to the fleet recorder safely.

        Truncates large results and re-raises critical exceptions (KeyboardInterrupt/SystemExit).
"""
if not (hasattr(self, "fleet") and self.fleet and hasattr(self.fleet, "recorder")):
            return
        try:
            if len(result_text) > 2000:
                result_text = result_text[:2000] + "... [TRUNCATED]"
            self.fleet.recorder.record_interaction(
                provider=provider,
                model="ShellCore",
                prompt=prompt,
                result=result_text,
                meta=meta,
            )
        except (RuntimeError, OSError, AttributeError, ValueError) as e:  # pragma: no cover - recorder errors
            # Non-critical failures are logged for telemetry debugging
            self.logger.debug("Failed to record shell interaction: %s", e)
    # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals


    async def execute_async(
        self,
        cmd: List[str],
        timeout: int = 120,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[Union[str, Path]] = None,
        capture_output: bool = True,
        sanitize: bool = True,
    ) -> ShellResult:
"""
Execute a command asynchronously.""
start_time = time.perf_counter()
        current_env = os.environ.copy()
        if env:
            current_env.update(env)

        if sanitize:
            current_env = self.sanitize_env(current_env)

        working_dir = cwd or self.repo_root

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE if capture_output else asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE if capture_output else asyncio.subprocess.DEVNULL,
                env=current_env,
                cwd=working_dir,
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(process.communicate(), timeout=timeout)
                stdout = stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
                stderr = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                res = ShellResult(cmd, -1, "", "Timeout expired", time.perf_counter() - start_time)
                prompt_trace = f"SHELL_EXECUTION_TIMEOUT: {' '.join(cmd)}"
                # Record the timeout event if recorder is available
                self._record_shell_interaction(
                    provider="shell",
                    prompt=prompt_trace,
                    result_text=str(res),
                    meta={"cmd": cmd, "cwd": str(working_dir), "duration": res.duration},
                )
                return res

            duration = time.perf_counter() - start_time
            res = ShellResult(
                command=cmd,
                returncode=process.returncode or 0,
                stdout=stdout,
                stderr=stderr,
                duration=duration,
            )
            # Record the shell execution to fleet recorder if available
            prompt_trace = f"SHELL_EXECUTION: {' '.join(cmd)}\nCWD: {working_dir}"
            result_text = res.stdout if res.stdout else res.stderr
            self._record_shell_interaction(
                provider="shell",
                prompt=prompt_trace,
                result_text=result_text,
                meta={"cmd": cmd, "cwd": str(working_dir), "duration": duration},
            )

            return res

        except (OSError, ValueError) as e:  # Expected runtime errors during process creation
            self.logger.error("Failed to execute %s: %s", cmd[0], e)
            prompt_trace = f"SHELL_EXECUTION_ASYNC_ERROR: {' '.join(cmd)}\nCWD: {working_dir}"
            self._record_shell_interaction(
                provider="shell",
                prompt=prompt_trace,
                result_text=str(e),
                meta={"cmd": cmd, "cwd": str(working_dir), "duration": time.perf_counter() - start_time},
            )
            return ShellResult(cmd, -2, "", str(e), time.perf_counter() - start_time)
    # pylint: disable=too-many-arguments,too-many-positional-arguments


    def execute(
        self,
        cmd: List[str],
        timeout: int = 120,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[Union[str, Path]] = None,
        check: bool = False,
    ) -> ShellResult:
"""
Execute a command synchronously.""
start_time = time.perf_counter()

        # Use Rust-accelerated directory walking if available
        if (
            rc
            and hasattr(rc, "execute_shell_rust")
            and not env
            and not cwd
        ):  # pylint: disable=no-member
            try:
                # Execution delegated to Rust for performance
                code, stdout, stderr = rc.execute_shell_rust(
                    cmd[0], cmd[1:]
                )  # type: ignore # pylint: disable=no-member
                return ShellResult(
                    command=cmd,
                    returncode=code,
                    stdout=stdout,
                    stderr=stderr,
                    duration=time.perf_counter() - start_time,
                )
            except RuntimeError as e:  # pylint: disable=broad-exception-caught, unused-variable
                self.logger.warning("Rust shell execution failed: %s", e)
        current_env = os.environ.copy()
        if env:
            current_env.update(env)

        working_dir = cwd or self.repo_root

        # Intelligence Gap: Record shell execution context for auditability
        self.logger.info(
            "Executing shell command: %s | cwd=%s | env_keys=%s", cmd, working_dir, list((env or {}).keys())
        )
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=current_env,
                cwd=working_dir,
                timeout=timeout,
                encoding="utf-8",
                errors="replace",
                check=check,
            )

            res = ShellResult(
                command=cmd,
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                duration=time.perf_counter() - start_time,
            )

            # Record the successful execution
            prompt_trace = f"SHELL_EXECUTION: {' '.join(cmd)}\nCWD: {working_dir}"
            result_text = res.stdout if res.stdout else res.stderr
            self._record_shell_interaction(
                provider="shell",
                prompt=prompt_trace,
                result_text=result_text,
                meta={"cmd": cmd, "cwd": str(working_dir), "duration": res.duration},
            )

            return res

        except subprocess.TimeoutExpired as e:
            res = ShellResult(
                command=cmd,
                returncode=-1,
                stdout=e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or ""),
                stderr=e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or ""),
                duration=time.perf_counter() - start_time,
            )
            prompt_trace = f"SHELL_EXECUTION_TIMEOUT: {' '.join(cmd)}\nCWD: {working_dir}"
            result_text = (res.stdout or res.stderr)
            self._record_shell_interaction(
                provider="shell",
                prompt=prompt_trace,
                result_text=result_text,
                meta={"cmd": cmd, "cwd": str(working_dir), "duration": res.duration},
            )
            return res
        except (OSError, ValueError) as e:
            self.logger.error("Failed to execute %s: %s", cmd[0], e)
            prompt_trace = f"SHELL_EXECUTION_ERROR: {' '.join(cmd)}\nCWD: {working_dir}"
            self._record_shell_interaction(
                provider="shell",
                prompt=prompt_trace,
                result_text=str(e),
                meta={"cmd": cmd, "cwd": str(working_dir), "duration": time.perf_counter() - start_time},
            )
            return ShellResult(cmd, -2, "", str(e), time.perf_counter() - start_time)
    def redact_command(self, cmd: List[str], sensitive_patterns: List[str]) -> List[str]:
        ""
Redact sensitive information from a command list for logging.""
redacted = []
        for part in cmd:
            for pattern in sensitive_patterns:
                part = part.replace(pattern, "********")
            redacted.append(part)
        return redacted
