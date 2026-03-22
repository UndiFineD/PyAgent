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

"""Acceptance tests for ProcessTransactionManager.

Test groups
-----------
Group A – src.core.ProcessTransactionManager shim (T08 required)
    TC-P1  shim import: ProcessTransaction + validate() importable
    TC-P2  validate() returns True
    TC-P3  start() creates _proc (Popen) with stdout=PIPE
    TC-P4  wait() returns integer returncode and sets tx.stdout bytes
    TC-P5  rollback() terminates a running process (_proc.poll() → not None)
    TC-P6  exception inside context triggers rollback → process terminated
    TC-P7  async start_async() + wait_async() → rc==0

Group B – src.transactions.ProcessTransactionManager full impl (T04 required)
    TC-P8  package import + validate() returns True
    TC-P9  async run() returns tuple (rc: int, stdout: str, stderr: str)
    TC-P10 async run() returncode equals what the process exited with
    TC-P11 async run() stdout captures printed output
    TC-P12 async rollback terminates async process (_async_proc terminated)
"""

from __future__ import annotations

import sys

import pytest

# ---------------------------------------------------------------------------
# Guard helpers
# ---------------------------------------------------------------------------

try:
    from src.core.ProcessTransactionManager import ProcessTransaction as _CoreProcessTx
    from src.core.ProcessTransactionManager import validate as _core_process_validate
    _HAS_CORE_PROCESS = True
except ImportError:
    _CoreProcessTx = None  # type: ignore[assignment,misc]
    _core_process_validate = None  # type: ignore[assignment]
    _HAS_CORE_PROCESS = False


def _skip_if_no_core_process() -> None:
    if not _HAS_CORE_PROCESS:
        pytest.skip("T08 pending: src.core.ProcessTransactionManager not yet created")


def _skip_if_no_tx_process() -> None:
    try:
        import src.transactions.ProcessTransactionManager  # noqa: F401
    except ImportError:
        pytest.skip("T04 pending: src.transactions.ProcessTransactionManager not yet created")


# ---------------------------------------------------------------------------
# Group A — src.core.ProcessTransactionManager shim
# ---------------------------------------------------------------------------

class TestProcessTransactionShim:
    """Tests against the shim at src.core.ProcessTransactionManager (T08)."""

    # TC-P1
    def test_shim_import_provides_process_transaction(self) -> None:
        """src.core.ProcessTransactionManager must export ProcessTransaction."""
        _skip_if_no_core_process()
        from src.core.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415
        assert ProcessTransaction is not None
        assert callable(ProcessTransaction)

    # TC-P2
    def test_shim_validate_returns_true(self) -> None:
        """Shim module must expose validate() → True."""
        _skip_if_no_core_process()
        from src.core.ProcessTransactionManager import validate  # noqa: PLC0415
        assert callable(validate)
        assert validate() is True

    # TC-P3
    def test_start_creates_popen_with_pipe(self) -> None:
        """start() must assign _proc as a Popen instance (stdout captured via PIPE)."""
        _skip_if_no_core_process()
        import subprocess  # noqa: PLC0415
        from src.core.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415

        cmd = [sys.executable, "-c", "import time; time.sleep(30)"]
        tx = ProcessTransaction(cmd)
        try:
            tx.start()
            assert tx._proc is not None, "_proc must be set after start()"
            assert isinstance(tx._proc, subprocess.Popen), "_proc must be a subprocess.Popen"
            assert tx._proc.stdout is not None, "_proc must have stdout captured (PIPE)"
        finally:
            # Always clean up the long-running process
            if tx._proc and tx._proc.poll() is None:
                tx._proc.kill()
                tx._proc.wait()

    # TC-P4
    def test_wait_returns_returncode_and_sets_stdout(self) -> None:
        """wait() must return the integer returncode and store bytes in tx.stdout."""
        _skip_if_no_core_process()
        from src.core.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415

        cmd = [sys.executable, "-c", "print('captured')"]
        with ProcessTransaction(cmd) as tx:
            tx.start()
            rc = tx.wait()

        assert isinstance(rc, int), f"wait() must return int, got {type(rc)}"
        assert rc == 0, f"Echo process must exit with 0, got {rc}"
        assert tx.stdout is not None, "tx.stdout must be set to bytes after wait()"
        assert b"captured" in tx.stdout, (
            f"tx.stdout must contain printed output, got {tx.stdout!r}"
        )

    # TC-P5
    def test_rollback_terminates_running_process(self) -> None:
        """rollback() must terminate a running subprocess (_proc.poll() returns not-None)."""
        _skip_if_no_core_process()
        from src.core.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415

        cmd = [sys.executable, "-c", "import time; time.sleep(30)"]
        tx = ProcessTransaction(cmd)
        tx.start()

        assert tx._proc is not None, "_proc must exist"
        assert tx._proc.poll() is None, "Process must be running before rollback"
        tx.rollback()
        assert tx._proc.poll() is not None, (
            "_proc must be terminated after rollback (poll() returns non-None)"
        )

    # TC-P6
    def test_exception_in_context_triggers_rollback(self) -> None:
        """Exception inside the with-block must trigger rollback → process terminated."""
        _skip_if_no_core_process()
        from src.core.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415

        cmd = [sys.executable, "-c", "import time; time.sleep(30)"]
        proc_holder: list = []

        with pytest.raises(ValueError):
            with ProcessTransaction(cmd) as tx:
                proc_holder.append(tx)
                tx.start()
                raise ValueError("abort-test")

        held = proc_holder[0]
        assert held._proc is not None, "_proc must have been assigned"
        assert held._proc.poll() is not None, (
            "Process must be dead after context-manager exception triggered rollback"
        )

    # TC-P7
    @pytest.mark.asyncio
    async def test_async_start_and_wait_returns_zero(self) -> None:
        """start_async() + wait_async() must complete successfully with rc==0."""
        _skip_if_no_core_process()
        from src.core.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415

        cmd = [sys.executable, "-c", "import sys; sys.exit(0)"]
        async with ProcessTransaction(cmd) as tx:
            await tx.start_async()
            rc = await tx.wait_async(timeout=10.0)

        assert rc == 0, f"Async wait must return 0 for a successful process, got {rc}"


# ---------------------------------------------------------------------------
# Group B — src.transactions.ProcessTransactionManager full implementation
# ---------------------------------------------------------------------------

class TestProcessTransactionFull:
    """Tests against the full src.transactions.ProcessTransactionManager (T04)."""

    # TC-P8
    def test_package_import_and_validate(self) -> None:
        """src.transactions.ProcessTransactionManager must export ProcessTransaction + validate()."""
        _skip_if_no_tx_process()
        from src.transactions.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415
        from src.transactions.ProcessTransactionManager import validate  # noqa: PLC0415

        assert ProcessTransaction is not None
        assert callable(validate)
        assert validate() is True

    # TC-P9
    @pytest.mark.asyncio
    async def test_async_run_returns_three_tuple(self) -> None:
        """run() must return a (int, str, str) tuple: (returncode, stdout, stderr)."""
        _skip_if_no_tx_process()
        from src.transactions.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415

        cmd = [sys.executable, "-c", "import sys; sys.exit(0)"]
        tx = ProcessTransaction()
        result = await tx.run(cmd)

        assert isinstance(result, tuple), f"run() must return tuple, got {type(result)}"
        assert len(result) == 3, f"run() tuple must have 3 elements, got {len(result)}"
        rc, stdout, stderr = result
        assert isinstance(rc, int), f"returncode must be int, got {type(rc)}"
        assert isinstance(stdout, str), f"stdout must be str, got {type(stdout)}"
        assert isinstance(stderr, str), f"stderr must be str, got {type(stderr)}"

    # TC-P10
    @pytest.mark.asyncio
    async def test_async_run_returncode_matches_exit_status(self) -> None:
        """run() returncode must match the process exit status exactly."""
        _skip_if_no_tx_process()
        from src.transactions.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415

        cmd_zero = [sys.executable, "-c", "import sys; sys.exit(0)"]
        cmd_nonzero = [sys.executable, "-c", "import sys; sys.exit(42)"]

        tx = ProcessTransaction()
        rc_zero, _, _ = await tx.run(cmd_zero)
        assert rc_zero == 0, f"Expected rc=0 for sys.exit(0), got {rc_zero}"

        rc_42, _, _ = await tx.run(cmd_nonzero)
        assert rc_42 == 42, f"Expected rc=42 for sys.exit(42), got {rc_42}"

    # TC-P11
    @pytest.mark.asyncio
    async def test_async_run_stdout_captures_output(self) -> None:
        """run() must capture process stdout in the returned string."""
        _skip_if_no_tx_process()
        from src.transactions.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415

        cmd = [sys.executable, "-c", "print('hello-stdout-capture')"]
        tx = ProcessTransaction()
        rc, stdout, _ = await tx.run(cmd)

        assert rc == 0
        assert "hello-stdout-capture" in stdout, (
            f"stdout must contain printed text, got {stdout!r}"
        )

    # TC-P12
    @pytest.mark.asyncio
    async def test_async_rollback_terminates_async_process(self) -> None:
        """rollback() must terminate an asyncio subprocess that is still running."""
        _skip_if_no_tx_process()
        from src.transactions.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415

        cmd = [sys.executable, "-c", "import time; time.sleep(30)"]
        tx = ProcessTransaction()
        await tx.start_async()

        assert tx._async_proc is not None, "_async_proc must be set after start_async()"
        assert tx._async_proc.returncode is None, "Process must still be running"
        await tx.rollback()
        assert tx._async_proc.returncode is not None, (
            "_async_proc must be terminated after async rollback"
        )
