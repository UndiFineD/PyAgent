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

"""Tests for StorageTransactionManager, ProcessTransactionManager, and ContextTransactionManager."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

from src.core.StorageTransactionManager import StorageTransaction
from src.core.ProcessTransactionManager import ProcessTransaction
from src.core.ContextTransactionManager import ContextTransaction, RecursionGuardError


# ---------------------------------------------------------------------------
# StorageTransaction tests
# ---------------------------------------------------------------------------


class TestStorageTransaction:
    """Tests for StorageTransaction context manager."""
    
    def test_commit_writes_file(self, tmp_path: Path) -> None:
        target = tmp_path / "output.bin"
        with StorageTransaction(target) as tx:
            tx.stage(b"hello world")
            tx.commit()
        assert target.read_bytes() == b"hello world"

    def test_rollback_on_exception_leaves_target_untouched(self, tmp_path: Path) -> None:
        target = tmp_path / "safe.txt"
        target.write_bytes(b"original")
        with pytest.raises(ValueError):
            with StorageTransaction(target) as tx:
                tx.stage(b"corrupted")
                raise ValueError("abort")
        assert target.read_bytes() == b"original"

    def test_autocommit_when_no_exception(self, tmp_path: Path) -> None:
        """Exit without explicit commit — __exit__ auto-commits."""
        target = tmp_path / "auto.txt"
        with StorageTransaction(target) as tx:
            tx.stage(b"auto-committed")
        assert target.read_bytes() == b"auto-committed"

    def test_stage_replaces_previous_stage(self, tmp_path: Path) -> None:
        target = tmp_path / "multi.txt"
        with StorageTransaction(target) as tx:
            tx.stage(b"first")
            tx.stage(b"second")
            tx.commit()
        assert target.read_bytes() == b"second"

    @pytest.mark.asyncio
    async def test_async_context_manager_commits(self, tmp_path: Path) -> None:
        target = tmp_path / "async_out.txt"
        async with StorageTransaction(target) as tx:
            tx.stage(b"async content")
            tx.commit()
        assert target.read_bytes() == b"async content"


# ---------------------------------------------------------------------------
# ProcessTransaction tests
# ---------------------------------------------------------------------------


class TestProcessTransaction:
    def test_start_and_wait_success(self) -> None:
        cmd = [sys.executable, "-c", "print('ok')"]
        with ProcessTransaction(cmd) as tx:
            tx.start()
            rc = tx.wait()
        assert rc == 0
        assert b"ok" in (tx.stdout or b"")

    def test_rollback_terminates_process(self) -> None:
        """A running process is terminated on rollback."""
        cmd = [sys.executable, "-c", "import time; time.sleep(30)"]
        tx = ProcessTransaction(cmd)
        tx.start()
        assert tx._proc is not None
        assert tx._proc.poll() is None  # running
        tx.rollback()
        # After rollback the process should be dead
        assert tx._proc.poll() is not None

    def test_exception_triggers_rollback(self) -> None:
        cmd = [sys.executable, "-c", "import time; time.sleep(30)"]
        proc_ref: list[ProcessTransaction] = []
        with pytest.raises(RuntimeError):
            with ProcessTransaction(cmd) as tx:
                proc_ref.append(tx)
                tx.start()
                raise RuntimeError("forced abort")
        assert proc_ref[0]._proc is not None
        assert proc_ref[0]._proc.poll() is not None

    @pytest.mark.asyncio
    async def test_async_start_and_wait(self) -> None:
        cmd = [sys.executable, "-c", "import sys; sys.exit(0)"]
        async with ProcessTransaction(cmd) as tx:
            await tx.start_async()
            rc = await tx.wait_async(timeout=5.0)
        assert rc == 0


# ---------------------------------------------------------------------------
# ContextTransaction tests
# ---------------------------------------------------------------------------


class TestContextTransaction:
    def test_basic_enter_exit(self) -> None:
        with ContextTransaction("task-1") as ctx:
            assert "task-1" in ContextTransaction.active_contexts()
        assert "task-1" not in ContextTransaction.active_contexts()

    def test_recursive_entry_raises(self) -> None:
        with ContextTransaction("task-loop"):
            with pytest.raises(RecursionGuardError):
                with ContextTransaction("task-loop"):
                    pass

    def test_different_contexts_nest_fine(self) -> None:
        with ContextTransaction("outer"):
            with ContextTransaction("inner"):
                active = ContextTransaction.active_contexts()
                assert "outer" in active
                assert "inner" in active

    def test_empty_context_id_raises(self) -> None:
        with pytest.raises(ValueError):
            ContextTransaction("")

    @pytest.mark.asyncio
    async def test_async_context_manager(self) -> None:
        async with ContextTransaction("async-task") as ctx:
            assert "async-task" in ContextTransaction.active_contexts()
        assert "async-task" not in ContextTransaction.active_contexts()
