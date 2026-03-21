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

"""Red-phase tests for unified transaction manager contracts."""

from __future__ import annotations

import importlib
from types import ModuleType


def _load_unified_module() -> ModuleType:
    """Load the expected unified transaction module for contract validation."""
    return importlib.import_module("src.core.UnifiedTransactionManager")


def test_unified_manager_class_contract_exists() -> None:
    """UnifiedTransactionManager class must exist with core lifecycle methods."""
    module = _load_unified_module()

    manager_cls = module.UnifiedTransactionManager
    required_methods = ["begin", "execute", "commit", "rollback"]

    for method_name in required_methods:
        assert hasattr(manager_cls, method_name), f"missing method: {method_name}"


def test_transaction_envelope_and_result_contracts_exist() -> None:
    """TransactionEnvelope and OperationResult contracts must be defined."""
    module = _load_unified_module()

    envelope_cls = module.TransactionEnvelope
    result_cls = module.OperationResult

    assert envelope_cls is not None
    assert result_cls is not None


def test_rollback_called_in_reverse_order_on_failure() -> None:
    """Manager must rollback completed operations in reverse order after a failure."""
    module = _load_unified_module()
    manager_cls = module.UnifiedTransactionManager

    manager = manager_cls()

    operations = [
        {"id": "op1", "adapter": "memory", "action": "set"},
        {"id": "op2", "adapter": "file", "action": "write"},
        {"id": "op3", "adapter": "process", "action": "spawn"},
    ]

    tx_id = manager.begin(operations=operations)

    # The expected behavior is that execution raises and rollback is performed.
    try:
        manager.execute(tx_id=tx_id, fail_on_operation_id="op2")
    except Exception:
        pass

    assert manager.rollback_log == ["op1"], "rollback should run for committed ops in reverse order"


def test_operation_error_metadata_is_exposed() -> None:
    """Errors must include domain and operation id metadata."""
    module = _load_unified_module()
    manager_cls = module.UnifiedTransactionManager

    manager = manager_cls()
    tx_id = manager.begin(operations=[{"id": "op-x", "adapter": "context", "action": "set"}])

    try:
        manager.execute(tx_id=tx_id, fail_on_operation_id="op-x")
    except Exception as exc:
        metadata = getattr(exc, "metadata", {})
        assert metadata.get("operation_id") == "op-x"
        assert metadata.get("adapter") == "context"
        return

    raise AssertionError("execute was expected to raise on failing operation")
