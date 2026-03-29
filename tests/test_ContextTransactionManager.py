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

"""Acceptance tests for ContextTransactionManager.

Test groups
-----------
Group A – src.core.ContextTransactionManager shim (T09 required)
    TC-C1  shim import: ContextTransaction, RecursionGuardError, validate() importable
    TC-C2  validate() returns True
    TC-C3  transaction_id is a uuid.UUID assigned automatically on construction
    TC-C4  nested contexts have parent_id pointing to outer transaction_id
    TC-C5  active_contexts() classmethod reflects entering and exiting
    TC-C6  RecursionGuardError raised when same context_id entered recursively
    TC-C7  ValueError raised for empty context_id
    TC-C8  current() classmethod returns innermost ContextTransaction from stack
    TC-C9  async with ContextTransaction enters and exits cleanly

Group B – src.transactions.ContextTransactionManager full impl (T05 required)
    TC-C10 package import + validate() returns True
    TC-C11 UUID lineage: outer.parent_id is None, inner.parent_id == outer.transaction_id
    TC-C12 current() returns None when no context is active
    TC-C13 RecursionGuardError clears context on propagation (no state leak)
"""

from __future__ import annotations

import uuid

import pytest

# ---------------------------------------------------------------------------
# Guard helpers
# ---------------------------------------------------------------------------

try:
    from src.core.ContextTransactionManager import ContextTransaction as _CoreContextTx
    from src.core.ContextTransactionManager import RecursionGuardError as _CoreRecursionGuardError
    from src.core.ContextTransactionManager import validate as _core_context_validate

    _HAS_CORE_CONTEXT = True
except ImportError:
    _CoreContextTx = None  # type: ignore[assignment,misc]
    _CoreRecursionGuardError = None  # type: ignore[assignment]
    _core_context_validate = None  # type: ignore[assignment]
    _HAS_CORE_CONTEXT = False


def _skip_if_no_core_context() -> None:
    if not _HAS_CORE_CONTEXT:
        pytest.skip("T09 pending: src.core.ContextTransactionManager not yet created")


def _skip_if_no_tx_context() -> None:
    try:
        import src.transactions.ContextTransactionManager  # noqa: F401
    except ImportError:
        pytest.skip("T05 pending: src.transactions.ContextTransactionManager not yet created")


# ---------------------------------------------------------------------------
# Group A — src.core.ContextTransactionManager shim
# ---------------------------------------------------------------------------


class TestContextTransactionShim:
    """Tests against the shim at src.core.ContextTransactionManager (T09)."""

    # TC-C1
    def test_shim_exports_context_transaction_and_recursion_guard_error(self) -> None:
        """Shim must export ContextTransaction and RecursionGuardError."""
        _skip_if_no_core_context()
        from src.core.ContextTransactionManager import (  # noqa: PLC0415
            ContextTransaction,
            RecursionGuardError,
        )

        assert ContextTransaction is not None
        assert callable(ContextTransaction)
        assert issubclass(RecursionGuardError, Exception)

    # TC-C2
    def test_shim_validate_returns_true(self) -> None:
        """Shim module must expose validate() → True."""
        _skip_if_no_core_context()
        from src.core.ContextTransactionManager import validate  # noqa: PLC0415

        assert callable(validate)
        assert validate() is True

    # TC-C3
    def test_transaction_id_is_uuid4_on_construction(self) -> None:
        """Each ContextTransaction must receive a unique UUID4 transaction_id automatically."""
        _skip_if_no_core_context()
        from src.core.ContextTransactionManager import ContextTransaction  # noqa: PLC0415

        tx1 = ContextTransaction("ctx-uuid-test-1")
        tx2 = ContextTransaction("ctx-uuid-test-2")

        assert hasattr(tx1, "transaction_id"), "transaction_id attribute must exist"
        assert isinstance(tx1.transaction_id, uuid.UUID), (
            f"transaction_id must be uuid.UUID, got {type(tx1.transaction_id)}"
        )
        assert tx1.transaction_id != tx2.transaction_id, "Each ContextTransaction must have a unique transaction_id"

    # TC-C4
    def test_nested_context_has_parent_id_linked_to_outer(self) -> None:
        """Inner ContextTransaction's parent_id must equal the outer's transaction_id."""
        _skip_if_no_core_context()
        from src.core.ContextTransactionManager import ContextTransaction  # noqa: PLC0415

        with ContextTransaction("parent-ctx") as outer:
            inner = ContextTransaction("child-ctx")
            inner.__enter__()
            try:
                assert hasattr(inner, "parent_id"), "parent_id attribute must exist"
                assert inner.parent_id == outer.transaction_id, (
                    f"inner.parent_id {inner.parent_id!r} must equal outer.transaction_id {outer.transaction_id!r}"
                )
            finally:
                inner.__exit__(None, None, None)

    # TC-C5
    def test_active_contexts_reflects_enter_and_exit(self) -> None:
        """active_contexts() must include context_id while active and exclude it after exit."""
        _skip_if_no_core_context()
        from src.core.ContextTransactionManager import ContextTransaction  # noqa: PLC0415

        context_id = "active-ctx-tracking"
        assert context_id not in ContextTransaction.active_contexts(), (
            "context_id must not be in active_contexts before entering"
        )

        with ContextTransaction(context_id):
            assert context_id in ContextTransaction.active_contexts(), (
                "context_id must be in active_contexts while inside with-block"
            )

        assert context_id not in ContextTransaction.active_contexts(), (
            "context_id must be removed from active_contexts after exiting"
        )

    # TC-C6
    def test_recursion_guard_error_on_reentrant_context_id(self) -> None:
        """Entering the same context_id while already active must raise RecursionGuardError."""
        _skip_if_no_core_context()
        from src.core.ContextTransactionManager import ContextTransaction, RecursionGuardError  # noqa: PLC0415

        with ContextTransaction("re-entrant"):
            with pytest.raises(RecursionGuardError):
                with ContextTransaction("re-entrant"):
                    pass

    # TC-C7
    def test_empty_context_id_raises_value_error(self) -> None:
        """ContextTransaction("") must raise ValueError immediately (not deferred)."""
        _skip_if_no_core_context()
        from src.core.ContextTransactionManager import ContextTransaction  # noqa: PLC0415

        with pytest.raises(ValueError):
            ContextTransaction("")

    # TC-C8
    def test_current_classmethod_returns_innermost(self) -> None:
        """current() must return the innermost active ContextTransaction from the stack."""
        _skip_if_no_core_context()
        from src.core.ContextTransactionManager import ContextTransaction  # noqa: PLC0415

        if not hasattr(ContextTransaction, "current"):
            pytest.skip("current() classmethod not yet implemented on shim (T09 pending)")

        with ContextTransaction("outer-current") as outer:
            assert ContextTransaction.current() is outer, (
                "current() must return the only active context when no nesting"
            )
            with ContextTransaction("inner-current") as inner:
                assert ContextTransaction.current() is inner, "current() must return innermost context when nested"
            assert ContextTransaction.current() is outer, "current() must revert to outer after inner exits"

    # TC-C9
    @pytest.mark.asyncio
    async def test_async_context_manager_enters_and_exits(self) -> None:
        """Async with ContextTransaction must track context_id in active_contexts."""
        _skip_if_no_core_context()
        from src.core.ContextTransactionManager import ContextTransaction  # noqa: PLC0415

        context_id = "async-ctx-test"
        async with ContextTransaction(context_id) as ctx:
            assert context_id in ContextTransaction.active_contexts(), (
                "context_id must be tracked during async with block"
            )
            assert isinstance(ctx, ContextTransaction)

        assert context_id not in ContextTransaction.active_contexts(), (
            "context_id must be removed after async with exits"
        )


# ---------------------------------------------------------------------------
# Group B — src.transactions.ContextTransactionManager full implementation
# ---------------------------------------------------------------------------


class TestContextTransactionFull:
    """Tests against the full src.transactions.ContextTransactionManager (T05)."""

    # TC-C10
    def test_package_import_and_validate(self) -> None:
        """src.transactions.ContextTransactionManager must export ContextTransaction + validate()."""
        _skip_if_no_tx_context()
        from src.transactions.ContextTransactionManager import (
            ContextTransaction,  # noqa: PLC0415
            validate,  # noqa: PLC0415
        )

        assert ContextTransaction is not None
        assert callable(validate)
        assert validate() is True

    # TC-C11
    def test_uuid_lineage_outer_has_no_parent_inner_linked(self) -> None:
        """Outer context must have parent_id=None; inner must inherit outer's transaction_id."""
        _skip_if_no_tx_context()
        from src.transactions.ContextTransactionManager import ContextTransaction  # noqa: PLC0415

        with ContextTransaction("outer-lineage") as outer:
            assert outer.parent_id is None, f"Top-level context must have parent_id=None, got {outer.parent_id!r}"
            with ContextTransaction("inner-lineage") as inner:
                assert inner.parent_id == outer.transaction_id, (
                    "inner.parent_id must equal outer.transaction_id for proper lineage"
                )

    # TC-C12
    def test_current_returns_none_when_no_active_context(self) -> None:
        """current() must return None when no ContextTransaction is active."""
        _skip_if_no_tx_context()
        from src.transactions.ContextTransactionManager import ContextTransaction  # noqa: PLC0415

        # Ensure no leftover state from other tests; call current() in isolation
        result = ContextTransaction.current()
        assert result is None, f"current() must return None when no context is active, got {result!r}"

    # TC-C13
    def test_recursion_guard_leaves_no_state_leak_after_error(self) -> None:
        """After RecursionGuardError, the context ID must still appear in active_contexts
        (the outer context is still active) but re-entry must still be guarded.
        """
        _skip_if_no_tx_context()
        from src.transactions.ContextTransactionManager import (  # noqa: PLC0415
            ContextTransaction,
            RecursionGuardError,
        )

        context_id = "no-leak"
        with ContextTransaction(context_id) as _outer:  # noqa: F841
            with pytest.raises(RecursionGuardError):
                with ContextTransaction(context_id):
                    pass  # should not reach

            # Outer context must still be active (no state leak)
            active = ContextTransaction.active_contexts()
            assert context_id in active, "Outer context must remain in active_contexts after RecursionGuardError"
            # And the recursion guard must still fire on a second attempt
            with pytest.raises(RecursionGuardError):
                with ContextTransaction(context_id):
                    pass

        # After outer exits, context must be cleared
        assert context_id not in ContextTransaction.active_contexts()
