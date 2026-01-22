<<<<<<< HEAD
<<<<<<< HEAD
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

"""Unified shell execution core for all PyAgent services."""

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
    """The result of a shell command execution."""

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified shell execution core for all PyAgent services."""

import os
import sys
import logging
import asyncio
import subprocess
import time
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass, field


try:
    import rust_core as rc
except ImportError:
    rc = None

@dataclass(frozen=True)
class ShellResult:
    """The result of a shell command execution."""
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    command: List[str]
    returncode: int
    stdout: str
    stderr: str
    duration: float
    success: bool = field(init=False)

<<<<<<< HEAD
<<<<<<< HEAD
    def __post_init__(self) -> None:
        # success is True if returncode is 0
        object.__setattr__(self, "success", self.returncode == 0)
=======
    def __post_init__(self):
        # success is True if returncode is 0
        object.__setattr__(self, 'success', self.returncode == 0)
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    def __post_init__(self):
        # success is True if returncode is 0
        object.__setattr__(self, 'success', self.returncode == 0)
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    def __str__(self) -> str:
        return f"ShellResult(rc={self.returncode}, success={self.success}, duration={self.duration:.2f}s)"


class ShellCore:
    """
    Centralized handler for shell and subprocess operations.
    Provides consistent logging, error handling, and environmental setup.
    """

<<<<<<< HEAD
<<<<<<< HEAD
    def __init__(self, repo_root: Optional[Union[str, Path]] = None) -> None:
=======
    def __init__(self, repo_root: Optional[Union[str, Path]] = None):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    def __init__(self, repo_root: Optional[Union[str, Path]] = None):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if repo_root:
            self.repo_root = Path(repo_root)
        else:
            try:
<<<<<<< HEAD
<<<<<<< HEAD
                from ..configuration.config_manager import \
                    CoreConfigManager  # pylint: disable=import-outside-toplevel

                # CoreConfigManager inherits from BaseCore which provides repo_root
                config = CoreConfigManager()
                self.repo_root = getattr(config, "repo_root", Path.cwd())
            except (ImportError, Exception):  # pylint: disable=unused-variable, broad-exception-caught
                self.repo_root = Path.cwd()

        self.logger = logging.getLogger("pyagent.shell")
        self._ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    def sanitize_env(self, env: Dict[str, str]) -> Dict[str, str]:
        """Filters environment variables to prevent secret leakage."""
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
        sanitized = {}
        for k, v in env.items():
            k_upper = k.upper()
            if k_upper in allow_list or k_upper.startswith("PYAGENT_") or k_upper.startswith("DV_"):
                sanitized[k] = v
        return sanitized
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                from src.core.base.configuration.config_manager import CoreConfigManager
                self.repo_root = CoreConfigManager().root_dir
            except ImportError:
                self.repo_root = Path.cwd()
            
        self.logger = logging.getLogger("pyagent.shell")
        self._ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    def execute(self, cmd: List[str], timeout: int = 120) -> ShellResult:
        """Synchronous execution, Rust-accelerated for high-speed spawning."""
        start_time = time.perf_counter()
        if rc and hasattr(rc, "execute_shell_rust"):
            try:
                code, stdout, stderr = rc.execute_shell_rust(cmd[0], cmd[1:])
                return ShellResult(
                    command=cmd,
                    returncode=code,
                    stdout=stdout,
                    stderr=stderr,
                    duration=time.perf_counter() - start_time
                )
            except Exception as e:
                self.logger.warning(f"Rust shell execution failed: {e}")
        
        # Python fallback
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return ShellResult(
            command=cmd,
            returncode=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            duration=time.perf_counter() - start_time
        )

    def sanitize_env(self, env: Dict[str, str]) -> Dict[str, str]:
        """Filters environment variables to prevent secret leakage."""
        allow_list = {
            "PATH", "PYTHONPATH", "LANG", "LC_ALL", "LC_CTYPE",
            "SYSTEMROOT", "WINDIR", "USERPROFILE", "HOME", "TEMP", "TMP",
            "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY",
            "AGENT_MODELS_CONFIG", "PYAGENT_ENV"
        }
        return {k: v for k, v in env.items() if k.upper() in allow_list}
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    def strip_ansi(self, text: str) -> str:
        """Removes ANSI escape sequences from a string."""
        if not text:
            return ""
        return self._ansi_escape.sub("", text)

<<<<<<< HEAD
<<<<<<< HEAD
    # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
    async def execute_async(
        self,
        cmd: List[str],
        timeout: int = 120,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[Union[str, Path]] = None,
        capture_output: bool = True,
        sanitize: bool = True,
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    async def execute_async(
        self, 
        cmd: List[str], 
        timeout: int = 120, 
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[Union[str, Path]] = None,
        capture_output: bool = True,
        sanitize: bool = True
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    ) -> ShellResult:
        """Execute a command asynchronously."""
        start_time = time.perf_counter()
        current_env = os.environ.copy()
        if env:
            current_env.update(env)
<<<<<<< HEAD
<<<<<<< HEAD

        if sanitize:
            current_env = self.sanitize_env(current_env)

        working_dir = cwd or self.repo_root

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            
        if sanitize:
            current_env = self.sanitize_env(current_env)
            
        working_dir = cwd or self.repo_root
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE if capture_output else asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE if capture_output else asyncio.subprocess.DEVNULL,
                env=current_env,
<<<<<<< HEAD
<<<<<<< HEAD
                cwd=working_dir,
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(process.communicate(), timeout=timeout)
                stdout = stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
                stderr = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                cwd=working_dir
            )
            
            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(process.communicate(), timeout=timeout)
                stdout = stdout_bytes.decode('utf-8', errors='replace') if stdout_bytes else ""
                stderr = stderr_bytes.decode('utf-8', errors='replace') if stderr_bytes else ""
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return ShellResult(cmd, -1, "", "Timeout expired", time.perf_counter() - start_time)

            return ShellResult(
                command=cmd,
                returncode=process.returncode or 0,
                stdout=stdout,
                stderr=stderr,
<<<<<<< HEAD
<<<<<<< HEAD
                duration=time.perf_counter() - start_time,
            )

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            self.logger.error("Failed to execute %s: %s", cmd[0], e)
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
        """Execute a command synchronously."""
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
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                self.logger.warning("Rust shell execution failed: %s", e)

        current_env = os.environ.copy()
        if env:
            current_env.update(env)

        working_dir = cwd or self.repo_root

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                duration=time.perf_counter() - start_time
            )
            
        except Exception as e:
            self.logger.error(f"Failed to execute {cmd[0]}: {e}")
            return ShellResult(cmd, -2, "", str(e), time.perf_counter() - start_time)

    def execute(
        self, 
        cmd: List[str], 
        timeout: int = 120, 
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[Union[str, Path]] = None,
        check: bool = False
    ) -> ShellResult:
        """Execute a command synchronously."""
        start_time = time.perf_counter()
        current_env = os.environ.copy()
        if env:
            current_env.update(env)
            
        working_dir = cwd or self.repo_root
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
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
<<<<<<< HEAD
<<<<<<< HEAD
                check=check,
            )

=======
                check=check
            )
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
                check=check
            )
            
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            return ShellResult(
                command=cmd,
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
<<<<<<< HEAD
<<<<<<< HEAD
                duration=time.perf_counter() - start_time,
            )

=======
                duration=time.perf_counter() - start_time
            )
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
                duration=time.perf_counter() - start_time
            )
            
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        except subprocess.TimeoutExpired as e:
            return ShellResult(
                command=cmd,
                returncode=-1,
                stdout=e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or ""),
                stderr=e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or ""),
<<<<<<< HEAD
<<<<<<< HEAD
                duration=time.perf_counter() - start_time,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            self.logger.error("Failed to execute %s: %s", cmd[0], e)
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                duration=time.perf_counter() - start_time
            )
        except Exception as e:
            self.logger.error(f"Failed to execute {cmd[0]}: {e}")
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            return ShellResult(cmd, -2, "", str(e), time.perf_counter() - start_time)

    def redact_command(self, cmd: List[str], sensitive_patterns: List[str]) -> List[str]:
        """Redact sensitive information from a command list for logging."""
        redacted = []
        for part in cmd:
            for pattern in sensitive_patterns:
                part = part.replace(pattern, "********")
            redacted.append(part)
        return redacted
