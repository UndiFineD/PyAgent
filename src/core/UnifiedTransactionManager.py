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

"""Minimal unified transaction contracts used by red-phase tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


def validate() -> bool:
    """Return True when unified transaction contracts are available."""
    return True


@dataclass(slots=True)
class TransactionEnvelope:
    """Envelope that tracks transaction identity and operations."""

    tx_id: str
    operations: list[dict[str, Any]]
    executed_operations: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class OperationResult:
    """Result contract for a single executed operation."""

    operation_id: str
    adapter: str
    success: bool


class UnifiedTransactionManager:
    """Simple in-memory transaction manager contract for red-phase validation."""

    def __init__(self) -> None:
        """Initialize the transaction manager with empty state."""
        self._transactions: dict[str, TransactionEnvelope] = {}
        self.rollback_log: list[str] = []

    def begin(self, operations: list[dict[str, Any]]) -> str:
        """Begin a new transaction with the given operations
        and return its transaction ID.
        """
        tx_id = str(uuid4())
        self._transactions[tx_id] = TransactionEnvelope(tx_id=tx_id, operations=list(operations))
        return tx_id

    def execute(self, tx_id: str, fail_on_operation_id: str | None = None) -> list[OperationResult]:
        """Execute the operations in the transaction envelope,
        optionally simulating a failure on a specific operation ID.
        """
        envelope = self._transactions[tx_id]
        failure_index = (
            next(
                (
                    idx
                    for idx, operation in enumerate(envelope.operations)
                    if str(operation.get("id", "")) == fail_on_operation_id
                ),
                None,
            )
            if fail_on_operation_id is not None
            else None
        )

        successful_operations = envelope.operations if failure_index is None else envelope.operations[:failure_index]

        envelope.executed_operations.extend(successful_operations)
        results = [
            OperationResult(
                operation_id=str(operation.get("id", "")),
                adapter=str(operation.get("adapter", "")),
                success=True,
            )
            for operation in successful_operations
        ]

        if failure_index is not None:
            failed_operation = envelope.operations[failure_index]
            operation_id = str(failed_operation.get("id", ""))
            adapter = str(failed_operation.get("adapter", ""))
            error = RuntimeError(f"operation failed: {operation_id}")
            error.metadata = {
                "operation_id": operation_id,
                "adapter": adapter,
            }
            self.rollback(tx_id)
            raise error

        return results

    def commit(self, tx_id: str) -> bool:
        """Commit the transaction and clear it from the manager."""
        self._transactions.pop(tx_id, None)
        return True

    def rollback(self, tx_id: str) -> bool:
        """Rollback the transaction and log the rolled-back operations."""
        envelope = self._transactions.get(tx_id)
        if envelope is None:
            return False

        self.rollback_log.extend([str(operation.get("id", "")) for operation in reversed(envelope.executed_operations)])

        envelope.executed_operations.clear()
        return True
