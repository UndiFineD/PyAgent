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

"""Acceptance tests for MemoryTransactionManager.

Test groups
-----------
Group A – src.MemoryTransactionManager (shim / current module, EXISTS NOW)
    TC-M1  import succeeds
    TC-M2  sync CM: RLock is reentrant from same thread (does not deadlock)
    TC-M3  sync CM: releases lock so a subsequent with-block can enter
    TC-M4  async CM: __aenter__/__aexit__ complete without error
    TC-M5  module-level validate() exists and returns True
           → FAILS until T10 (shim replacement) is done — AssertionError

Group B – src.transactions.MemoryTransactionManager (T06 required, NOT EXISTS)
    TC-M6  package import + validate() returns True
    TC-M7  upgraded set() / get() / delete() KV operations work
    TC-M8  commit() flushes _pending into _store
    TC-M9  rollback() discards _pending without touching _store
    TC-M10 sync_remote(dry_run=True) returns dict payload, no network call
"""

from __future__ import annotations

from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Group A — existing src.MemoryTransactionManager shim
# ---------------------------------------------------------------------------

from src.MemoryTransactionManager import MemoryTransaction  # must work NOW


class TestMemoryTransactionShim:
    """Tests against the existing src.MemoryTransactionManager module."""

    # TC-M1
    def test_import_memory_transaction(self) -> None:
        """MemoryTransaction must be importable from the shim path."""
        assert MemoryTransaction is not None
        assert callable(MemoryTransaction)

    # TC-M2
    def test_sync_context_manager_reentrant(self) -> None:
        """MemoryTransaction uses RLock: same thread must not deadlock on reentrance."""
        acquired_inner = False
        with MemoryTransaction() as tx_outer:
            with MemoryTransaction() as tx_inner:  # reentrant — must not deadlock
                acquired_inner = True
                assert tx_inner is not tx_outer
        assert acquired_inner is True

    # TC-M3
    def test_sync_context_manager_releases_lock(self) -> None:
        """Lock must be released on __exit__ so a second with-block can proceed."""
        with MemoryTransaction():
            pass  # first acquisition + release
        # After the first block exits, a second entry must succeed (not block)
        entered = False
        with MemoryTransaction():
            entered = True
        assert entered is True

    # TC-M4
    @pytest.mark.asyncio
    async def test_async_context_manager_completes(self) -> None:
        """async with MemoryTransaction() must enter and exit without raising."""
        entered = False
        async with MemoryTransaction() as tx:
            entered = True
            assert isinstance(tx, MemoryTransaction)
        assert entered is True

    # TC-M5
    def test_module_level_validate_exists_and_returns_true(self) -> None:
        """src.MemoryTransactionManager must expose validate() → True.

        EXPECTED FAILURE until T10 (shim replacement) is complete.
        AssertionError: Module-level validate() function not yet implemented.
        """
        import src.MemoryTransactionManager as _mod

        assert hasattr(_mod, "validate"), (
            "Module-level validate() not yet implemented on src.MemoryTransactionManager (T10 pending)"
        )
        assert callable(_mod.validate), "validate must be callable"
        assert _mod.validate() is True, "validate() must return True"


# ---------------------------------------------------------------------------
# Group B — src.transactions.MemoryTransactionManager (T06 required)
# ---------------------------------------------------------------------------

def _skip_if_no_tx_memory() -> None:
    """Skip the calling test if src.transactions.MemoryTransactionManager is absent."""
    try:
        import src.transactions.MemoryTransactionManager  # noqa: F401
    except ImportError:
        pytest.skip("T06 pending: src.transactions.MemoryTransactionManager not yet created")


class TestMemoryTransactionUpgraded:
    """Tests against the new src.transactions.MemoryTransactionManager implementation."""

    # TC-M6
    def test_package_import_and_validate(self) -> None:
        """src.transactions.MemoryTransactionManager must expose validate() → True."""
        _skip_if_no_tx_memory()
        from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415
        from src.transactions.MemoryTransactionManager import validate  # noqa: PLC0415

        assert callable(validate)
        assert validate() is True
        assert MTx is not None

    # TC-M7
    @pytest.mark.asyncio
    async def test_set_get_delete_key_value(self) -> None:
        """set/get/delete must manipulate the _pending store correctly."""
        _skip_if_no_tx_memory()
        from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415

        tx = MTx()
        await tx.set("alpha", 42)
        result = await tx.get("alpha")
        assert result == 42, f"Expected 42, got {result!r}"

        await tx.delete("alpha")
        missing = await tx.get("alpha")
        assert missing is None, f"Expected None after delete, got {missing!r}"

    # TC-M8
    @pytest.mark.asyncio
    async def test_commit_flushes_pending_into_store(self) -> None:
        """commit() must move _pending entries into _store."""
        _skip_if_no_tx_memory()
        from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415

        tx = MTx()
        await tx.set("key1", "value1")
        # Before commit: _pending has the value; _store may not
        assert "key1" not in tx._store, "_store should not yet contain uncommitted entry"  # type: ignore[union-attr]
        await tx.commit()
        assert "key1" in tx._store, "_store must contain entry after commit"  # type: ignore[union-attr]
        assert tx._store["key1"] == "value1"  # type: ignore[union-attr]

    # TC-M9
    @pytest.mark.asyncio
    async def test_rollback_discards_pending(self) -> None:
        """rollback() must discard _pending without changing _store."""
        _skip_if_no_tx_memory()
        from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415

        tx = MTx()
        await tx.set("discard_me", "oops")
        assert "discard_me" in tx._pending  # type: ignore[union-attr]
        await tx.rollback()
        assert "discard_me" not in tx._pending, "_pending must be cleared by rollback"  # type: ignore[union-attr]
        assert "discard_me" not in tx._store, "_store must be untouched by rollback"  # type: ignore[union-attr]

    # TC-M10
    @pytest.mark.asyncio
    async def test_sync_remote_dry_run_returns_payload_dict(self) -> None:
        """sync_remote(dry_run=True) must return a dict and not make a real network call."""
        _skip_if_no_tx_memory()
        from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415

        tx = MTx()
        await tx.set("k", "v")
        await tx.commit()
        payload = await tx.sync_remote("http://localhost:9999/sync", dry_run=True)
        assert isinstance(payload, dict), f"Expected dict payload from dry_run, got {type(payload)}"
        # payload must contain the committed store entry
        assert "k" in payload, "dry_run payload must include committed store keys"

    # TC-M11
    @pytest.mark.asyncio
    async def test_encrypt_decrypt_roundtrip_with_real_security_bridge(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """encrypt=True/decrypt=True must round-trip using the Rust security bridge."""
        _skip_if_no_tx_memory()
        from src.core import security_bridge  # noqa: PLC0415
        from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415

        key_file = tmp_path / "memory_key.b64"
        security_bridge.generate_key(key_file)
        monkeypatch.setenv("PYAGENT_MEMORY_KEY_FILE", str(key_file))

        tx = MTx()
        source = {"k": "v", "n": 7}
        await tx.set("secure", source, encrypt=True)
        raw = await tx.get("secure")
        assert isinstance(raw, dict)
        assert "__enc__" in raw

        decrypted = await tx.get("secure", decrypt=True)
        assert decrypted == source

    # TC-M12
    @pytest.mark.asyncio
    async def test_encrypt_without_key_file_env_raises_value_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """encrypt=True must fail fast when PYAGENT_MEMORY_KEY_FILE is not configured."""
        _skip_if_no_tx_memory()
        from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415

        monkeypatch.delenv("PYAGENT_MEMORY_KEY_FILE", raising=False)

        tx = MTx()
        with pytest.raises(ValueError, match="PYAGENT_MEMORY_KEY_FILE"):
            await tx.set("secure", "value", encrypt=True)
