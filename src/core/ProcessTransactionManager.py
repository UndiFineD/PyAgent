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

"""Process execution transaction manager.

:class:`ProcessTransaction` wraps a subprocess launched via
:mod:`asyncio` or :mod:`subprocess`.  It tracks the process handle so
that a rollback can terminate the process when an error occurs mid-task.

Both synchronous and asynchronous ``with`` blocks are supported.
"""

from __future__ import annotations

import asyncio
import subprocess
from typing import Any, Optional, Type


class ProcessTransaction:
    """Context manager that runs and tracks a subprocess.

    Parameters
    ----------
    cmd:
        Command and arguments to execute (same format as
        :func:`subprocess.run`).
    tid:
        Optional opaque transaction identifier for tracing.

    Usage (sync)::

        with ProcessTransaction(["echo", "hello"]) as tx:
            tx.start()
            tx.wait()
        # process finished normally, returncode accessible via tx.returncode

    Usage (async)::

        async with ProcessTransaction(["sleep", "1"]) as tx:
            await tx.start_async()
            await tx.wait_async()
    """

    def __init__(self, cmd: list[str], tid: Optional[Any] = None) -> None:
        self.cmd = cmd
        self.tid = tid
        self._proc: Optional[subprocess.Popen[bytes]] = None
        self._async_proc: Optional[asyncio.subprocess.Process] = None
        self.returncode: Optional[int] = None
        self.stdout: Optional[bytes] = None
        self.stderr: Optional[bytes] = None

    # ------------------------------------------------------------------
    # Public sync API
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Launch the subprocess (non-blocking)."""
        self._proc = subprocess.Popen(
            self.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def wait(self, timeout: Optional[float] = None) -> int:
        """Wait for the subprocess to finish and return its exit code."""
        if self._proc is None:
            raise RuntimeError("Process not started; call start() first")
        self.stdout, self.stderr = self._proc.communicate(timeout=timeout)
        self.returncode = self._proc.returncode
        return self.returncode

    def rollback(self) -> None:
        """Terminate the running subprocess if it is still alive."""
        if self._proc is not None and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._proc.kill()
        if self._async_proc is not None:
            try:
                self._async_proc.terminate()
            except ProcessLookupError:
                pass

    # ------------------------------------------------------------------
    # Public async API
    # ------------------------------------------------------------------

    async def start_async(self) -> None:
        """Launch the subprocess asynchronously (non-blocking)."""
        self._async_proc = await asyncio.create_subprocess_exec(
            *self.cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

    async def wait_async(self, timeout: Optional[float] = None) -> int:
        """Await subprocess completion and return its exit code."""
        if self._async_proc is None:
            raise RuntimeError("Process not started; call start_async() first")
        if timeout is not None:
            stdout, stderr = await asyncio.wait_for(
                self._async_proc.communicate(), timeout=timeout
            )
        else:
            stdout, stderr = await self._async_proc.communicate()
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = self._async_proc.returncode
        return self.returncode  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # Sync context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "ProcessTransaction":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[Any],
    ) -> None:
        if exc_type is not None:
            self.rollback()

    # ------------------------------------------------------------------
    # Async context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "ProcessTransaction":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[Any],
    ) -> None:
        if exc_type is not None:
            self.rollback()
