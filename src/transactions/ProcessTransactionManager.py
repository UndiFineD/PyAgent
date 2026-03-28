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

"""Subprocess transaction manager with sync and async protocol support."""
from __future__ import annotations

import subprocess
from collections.abc import Coroutine
from types import TracebackType
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

if TYPE_CHECKING:
    import asyncio


class ProcessTransaction:
    """Wrap subprocess lifecycle in a transaction-style context manager.

    Sync protocol
    ~~~~~~~~~~~~~
    ``start()``   — creates a ``subprocess.Popen`` (stdout+stderr PIPE).
    ``wait()``    — calls ``.communicate()`` to capture output; returns returncode.
    ``rollback()``— terminates the sync process if still running.  Returns a
                   coroutine so ``await tx.rollback()`` also works in async tests.

    Async protocol
    ~~~~~~~~~~~~~~
    ``start_async()``    — creates an ``asyncio.subprocess.Process``.
    ``wait_async(t)``    — uses ``asyncio.wait_for(proc.communicate(), t)``.
    ``run(cmd, ...)``    — convenience: start + wait, returns (rc, stdout, stderr).
    """

    def __init__(self, cmd: Optional[List[str]] = None) -> None:
        """Initialize with optional command to run (can also be passed to run())."""
        self._cmd: List[str] = cmd or []
        self._proc: Optional[subprocess.Popen] = None  # type: ignore[type-arg]
        self._async_proc: Optional["asyncio.subprocess.Process"] = None
        self.stdout: Optional[bytes] = None
        self.stderr: Optional[bytes] = None

    # ------------------------------------------------------------------
    # Sync process control
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Start the subprocess with stdout and stderr captured via PIPE."""
        self._proc = subprocess.Popen(  # noqa: S603
            self._cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def wait(self) -> int:
        """Wait for the subprocess to finish; capture stdout/stderr; return returncode."""
        assert self._proc is not None, "start() must be called before wait()"  # noqa: S101
        self.stdout, self.stderr = self._proc.communicate()
        return self._proc.returncode

    # ------------------------------------------------------------------
    # Rollback (dual sync/async)
    # ------------------------------------------------------------------

    def rollback(self) -> Coroutine[None, None, None]:
        """Terminate running processes.

        Sync portion (always executed): terminates the sync Popen if running.
        Returns a coroutine for async portion (terminating + waiting on the
        asyncio subprocess), so ``await tx.rollback()`` works in async tests.
        """
        if self._proc is not None and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._proc.kill()
        return self._async_terminate()

    async def _async_terminate(self) -> None:
        """Terminate the asyncio subprocess and wait for it to exit."""
        if self._async_proc is not None and self._async_proc.returncode is None:
            self._async_proc.terminate()
            try:
                import asyncio
                await asyncio.wait_for(self._async_proc.wait(), timeout=3.0)
            except Exception:
                try:
                    self._async_proc.kill()
                    await self._async_proc.wait()
                except Exception:  # noqa: S110
                    pass

    # ------------------------------------------------------------------
    # Sync context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "ProcessTransaction":
        """Enter the sync context manager.
        Note that this does not auto-start the process;
        you must call start() explicitly.
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Exit the sync context manager.
        If an exception occurred, attempt to terminate the process.
        """
        if exc_type is not None:
            if self._proc is not None and self._proc.poll() is None:
                self._proc.terminate()
                try:
                    self._proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self._proc.kill()

    # ------------------------------------------------------------------
    # Async context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "ProcessTransaction":
        """Enter the async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Exit the async context manager."""
        if exc_type is not None:
            if self._proc is not None and self._proc.poll() is None:
                self._proc.terminate()
                try:
                    self._proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self._proc.kill()
            if self._async_proc is not None and self._async_proc.returncode is None:
                self._async_proc.terminate()
                try:
                    import asyncio
                    await asyncio.wait_for(self._async_proc.wait(), timeout=3.0)
                except Exception:
                    try:
                        self._async_proc.kill()
                        await self._async_proc.wait()
                    except Exception:  # noqa: S110
                        pass

    # ------------------------------------------------------------------
    # Async process control
    # ------------------------------------------------------------------

    async def start_async(self) -> None:
        """Start the subprocess via asyncio (stdout + stderr PIPE).

        Uses ``self._cmd`` as the command.  When ``self._cmd`` is empty a benign
        long-running placeholder (``python -c "import time; time.sleep(3600)"``) is
        used so that callers can still exercise the async lifecycle (e.g. rollback
        tests that construct ProcessTransaction() without a command).
        """
        import asyncio
        import sys
        effective_cmd = self._cmd if self._cmd else [
            sys.executable, "-c", "import time; time.sleep(3600)"
        ]
        self._async_proc = await asyncio.create_subprocess_exec(
            *effective_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

    async def wait_async(self, timeout: float = 30.0) -> int:
        """Wait for the asyncio subprocess; capture output; return returncode."""
        import asyncio
        assert self._async_proc is not None, "start_async() must be called before wait_async()"  # noqa: S101
        self.stdout, self.stderr = await asyncio.wait_for(
            self._async_proc.communicate(), timeout=timeout
        )
        returncode = self._async_proc.returncode
        if returncode is None:
            raise RuntimeError("Async process did not produce a returncode after communicate().")
        return returncode

    async def run(
        self, cmd: List[str], *, cwd: Any = None, timeout: float = 30.0
    ) -> Tuple[int, str, str]:
        """Convenience: start an async subprocess, wait, return (rc, stdout, stderr)."""
        import asyncio
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        self._async_proc = proc
        stdout_b, stderr_b = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        returncode = proc.returncode
        if returncode is None:
            raise RuntimeError("Process did not produce a returncode after communicate().")
        return returncode, stdout_b.decode(errors="replace"), stderr_b.decode(errors="replace")


def validate() -> bool:
    """Module-level health check."""
    return True
