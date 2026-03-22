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

"""Subprocess guard: captures stdout/stderr and terminates on rollback."""

from __future__ import annotations

import asyncio
import subprocess
from types import TracebackType
from typing import Optional


def validate() -> bool:
    """Return True when ProcessTransaction contracts are available."""
    return True


class ProcessTransaction:
    """Wraps a subprocess with transactional lifecycle management.

    Usage (sync)::

        with ProcessTransaction(["python", "-c", "print('ok')"]) as tx:
            tx.start()
            rc = tx.wait()

    Usage (async)::

        async with ProcessTransaction(cmd) as tx:
            await tx.start_async()
            rc = await tx.wait_async(timeout=10.0)

    On exception the managed process is terminated (SIGTERM then SIGKILL).
    """

    def __init__(self, cmd: list[str]) -> None:
        self._cmd = cmd
        self._proc: Optional[subprocess.Popen] = None  # type: ignore[type-arg]
        self._async_proc: Optional[asyncio.subprocess.Process] = None
        self._stdout: Optional[bytes] = None
        self._stderr: Optional[bytes] = None

    # ------------------------------------------------------------------
    # Sync API
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Start the subprocess."""
        self._proc = subprocess.Popen(
            self._cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def wait(self) -> int:
        """Block until the process exits; return the return code."""
        if self._proc is None:
            raise RuntimeError("Process not started; call start() first.")
        stdout, stderr = self._proc.communicate()
        self._stdout = stdout
        self._stderr = stderr
        return self._proc.returncode

    @property
    def stdout(self) -> Optional[bytes]:
        """Captured stdout bytes after wait() completes."""
        return self._stdout

    @property
    def stderr(self) -> Optional[bytes]:
        """Captured stderr bytes after wait() completes."""
        return self._stderr

    def rollback(self) -> None:
        """Terminate the managed process if it is still running."""
        if self._proc is not None and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._proc.kill()
                self._proc.wait()

    # ------------------------------------------------------------------
    # Async API
    # ------------------------------------------------------------------

    async def start_async(self) -> None:
        """Start the subprocess asynchronously."""
        self._async_proc = await asyncio.create_subprocess_exec(
            *self._cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

    async def wait_async(self, timeout: float = 30.0) -> int:
        """Await process completion with an optional timeout; return return code."""
        if self._async_proc is None:
            raise RuntimeError("Process not started; call start_async() first.")
        try:
            stdout, stderr = await asyncio.wait_for(
                self._async_proc.communicate(), timeout=timeout
            )
        except asyncio.TimeoutError:
            self._async_proc.terminate()
            raise
        self._stdout = stdout
        self._stderr = stderr
        return self._async_proc.returncode

    async def _rollback_async(self) -> None:
        if self._async_proc is not None and self._async_proc.returncode is None:
            self._async_proc.terminate()
            try:
                await asyncio.wait_for(self._async_proc.wait(), timeout=5)
            except asyncio.TimeoutError:
                self._async_proc.kill()
                await self._async_proc.wait()

    # ------------------------------------------------------------------
    # Sync context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "ProcessTransaction":
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        if exc_type is not None:
            self.rollback()
        return False

    # ------------------------------------------------------------------
    # Async context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "ProcessTransaction":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        if exc_type is not None:
            await self._rollback_async()
        return False
