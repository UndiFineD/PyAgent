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

"""Acceptance tests for StorageTransactionManager.

Test groups
-----------
Group A – src.core.StorageTransactionManager shim (T07 required)
    TC-S1  shim import: StorageTransaction + validate() importable
    TC-S2  validate() returns True
    TC-S3  stage() + commit() writes file atomically (bytes match)
    TC-S4  rollback on exception leaves original file untouched
    TC-S5  double-commit raises an exception (CommitError or equivalent)
    TC-S6  staging with no prior stage → commit no-ops, no crash
    TC-S7  async with StorageTransaction: commit writes file

Group B – src.transactions.StorageTransactionManager full impl (T03 required)
    TC-S8  package import + validate() returns True
    TC-S9  async write() + acommit() creates file with correct content
    TC-S10 async rollback() removes written tmp file, target absent
    TC-S11 async delete() queued operation removes existing file on commit
    TC-S12 async mkdir() creates directory on commit
    TC-S13 encryption raises EncryptionConfigError when PYAGENT_STORAGE_MASTER_KEY absent
"""

from __future__ import annotations

from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Guard helpers
# ---------------------------------------------------------------------------

try:
    from src.core.StorageTransactionManager import StorageTransaction as _CoreStorageTx
    from src.core.StorageTransactionManager import validate as _core_storage_validate

    _HAS_CORE_STORAGE = True
except ImportError:
    _CoreStorageTx = None  # type: ignore[assignment,misc]
    _core_storage_validate = None  # type: ignore[assignment]
    _HAS_CORE_STORAGE = False


def _skip_if_no_core_storage() -> None:
    if not _HAS_CORE_STORAGE:
        pytest.skip("T07 pending: src.core.StorageTransactionManager not yet created")


def _skip_if_no_tx_storage() -> None:
    try:
        import src.transactions.StorageTransactionManager  # noqa: F401
    except ImportError:
        pytest.skip("T03 pending: src.transactions.StorageTransactionManager not yet created")


# ---------------------------------------------------------------------------
# Group A — src.core.StorageTransactionManager shim
# ---------------------------------------------------------------------------


class TestStorageTransactionShim:
    """Tests against the shim at src.core.StorageTransactionManager (T07)."""

    # TC-S1
    def test_shim_import_provides_storage_transaction(self) -> None:
        """src.core.StorageTransactionManager must export StorageTransaction."""
        _skip_if_no_core_storage()
        from src.core.StorageTransactionManager import StorageTransaction  # noqa: PLC0415

        assert StorageTransaction is not None
        assert callable(StorageTransaction)

    # TC-S2
    def test_shim_validate_returns_true(self) -> None:
        """Shim module must expose validate() → True."""
        _skip_if_no_core_storage()
        from src.core.StorageTransactionManager import validate  # noqa: PLC0415

        assert callable(validate)
        assert validate() is True

    # TC-S3
    def test_stage_and_commit_writes_bytes_to_target(self, tmp_path: Path) -> None:
        """stage(bytes) followed by commit() must write those exact bytes to the target path."""
        _skip_if_no_core_storage()
        from src.core.StorageTransactionManager import StorageTransaction  # noqa: PLC0415

        target = tmp_path / "output.bin"
        with StorageTransaction(target) as tx:
            tx.stage(b"data-payload-xyz")
            tx.commit()
        assert target.exists(), "Target file must exist after commit"
        assert target.read_bytes() == b"data-payload-xyz"

    # TC-S4
    def test_rollback_on_exception_leaves_original_file(self, tmp_path: Path) -> None:
        """An exception inside the context triggers rollback; original content must survive."""
        _skip_if_no_core_storage()
        from src.core.StorageTransactionManager import StorageTransaction  # noqa: PLC0415

        target = tmp_path / "safe.bin"
        original = b"original-content"
        target.write_bytes(original)

        with pytest.raises(RuntimeError):
            with StorageTransaction(target) as tx:
                tx.stage(b"corrupted-overwrite")
                raise RuntimeError("simulated abort")

        assert target.read_bytes() == original, "Rollback must not overwrite the original file on exception"

    # TC-S5
    def test_double_commit_raises(self, tmp_path: Path) -> None:
        """Calling commit() a second time on an already-committed tx must raise."""
        _skip_if_no_core_storage()
        from src.core.StorageTransactionManager import StorageTransaction  # noqa: PLC0415

        target = tmp_path / "once.bin"
        tx = StorageTransaction(target)
        tx.stage(b"first-write")
        tx.commit()  # first commit succeeds

        with pytest.raises(Exception):  # CommitError or ValueError or similar
            tx.commit()  # second commit must raise

    # TC-S6
    def test_commit_without_stage_does_not_crash(self, tmp_path: Path) -> None:
        """A commit() with nothing staged must be a safe no-op (no target created)."""
        _skip_if_no_core_storage()
        from src.core.StorageTransactionManager import StorageTransaction  # noqa: PLC0415

        target = tmp_path / "never.bin"
        with StorageTransaction(target) as tx:
            tx.commit()  # no stage issued
        # Target should not exist (nothing was staged)
        assert not target.exists(), "Unstaged commit must not create the target file"

    # TC-S7
    @pytest.mark.asyncio
    async def test_async_context_manager_commits(self, tmp_path: Path) -> None:
        """Async with StorageTransaction should commit cleanly on normal exit."""
        _skip_if_no_core_storage()
        from src.core.StorageTransactionManager import StorageTransaction  # noqa: PLC0415

        target = tmp_path / "async_write.bin"
        async with StorageTransaction(target) as tx:
            tx.stage(b"async-bytes")
            tx.commit()
        assert target.exists(), "Target must exist after async context manager exits"
        assert target.read_bytes() == b"async-bytes"


# ---------------------------------------------------------------------------
# Group B — src.transactions.StorageTransactionManager full implementation
# ---------------------------------------------------------------------------


class TestStorageTransactionFull:
    """Tests against the full src.transactions.StorageTransactionManager (T03)."""

    # TC-S8
    def test_package_import_and_validate(self) -> None:
        """src.transactions.StorageTransactionManager must export StorageTransaction + validate()."""
        _skip_if_no_tx_storage()
        from src.transactions.StorageTransactionManager import (
            StorageTransaction,  # noqa: PLC0415
            validate,  # noqa: PLC0415
        )

        assert StorageTransaction is not None
        assert callable(validate)
        assert validate() is True

    # TC-S9
    @pytest.mark.asyncio
    async def test_async_write_and_acommit_creates_file(self, tmp_path: Path) -> None:
        """write() followed by acommit() must create the target file with exact content."""
        _skip_if_no_tx_storage()
        from src.transactions.StorageTransactionManager import StorageTransaction  # noqa: PLC0415

        target = tmp_path / "async_new.bin"
        async with StorageTransaction() as tx:
            await tx.write(target, b"new-async-content")
            await tx.acommit()
        assert target.exists(), "Target must exist after async write + acommit"
        assert target.read_bytes() == b"new-async-content"

    # TC-S10
    @pytest.mark.asyncio
    async def test_async_rollback_removes_tmp_target_absent(self, tmp_path: Path) -> None:
        """Rolling back an async write must leave the target absent (no partial write)."""
        _skip_if_no_tx_storage()
        from src.transactions.StorageTransactionManager import StorageTransaction  # noqa: PLC0415

        target = tmp_path / "rollback_me.bin"
        tx = StorageTransaction()
        await tx.__aenter__()
        await tx.write(target, b"ephemeral")
        await tx.rollback()
        await tx.__aexit__(None, None, None)

        assert not target.exists(), "After rollback the target must not exist (tmp file removed, no commit)"

    # TC-S11
    @pytest.mark.asyncio
    async def test_async_delete_removes_existing_file(self, tmp_path: Path) -> None:
        """delete() queued then acommit() must remove an existing file."""
        _skip_if_no_tx_storage()
        from src.transactions.StorageTransactionManager import StorageTransaction  # noqa: PLC0415

        target = tmp_path / "to_delete.bin"
        target.write_bytes(b"exists")

        async with StorageTransaction() as tx:
            await tx.delete(target)
            await tx.acommit()

        assert not target.exists(), "File must be absent after delete op committed"

    # TC-S12
    @pytest.mark.asyncio
    async def test_async_mkdir_creates_directory(self, tmp_path: Path) -> None:
        """mkdir() committed via acommit() must create the directory on disk."""
        _skip_if_no_tx_storage()
        from src.transactions.StorageTransactionManager import StorageTransaction  # noqa: PLC0415

        new_dir = tmp_path / "new_dir" / "nested"
        async with StorageTransaction() as tx:
            await tx.mkdir(new_dir)
            await tx.acommit()

        assert new_dir.is_dir(), f"Directory {new_dir} must exist after mkdir+acommit"

    # TC-S13
    @pytest.mark.asyncio
    async def test_encryption_raises_without_master_key(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """write() with user_id set must raise EncryptionConfigError when env key absent."""
        _skip_if_no_tx_storage()
        monkeypatch.delenv("PYAGENT_STORAGE_MASTER_KEY", raising=False)

        try:
            from src.transactions.StorageTransactionManager import (  # noqa: PLC0415
                EncryptionConfigError,
                StorageTransaction,
            )
        except ImportError:
            pytest.skip("EncryptionConfigError not yet defined in transactions package")

        target = tmp_path / "secret.bin"
        with pytest.raises(EncryptionConfigError):
            async with StorageTransaction() as tx:
                await tx.write(target, b"secret", user_id="test-user")
