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

"""Shadow execution core for side-effect-free replay execution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .exceptions import ReplayConfigurationError, ShadowPolicyViolation
from .ReplayEnvelope import ReplayEnvelope


@dataclass
class ReplayStepResult:
    """Structured execution result for one replay envelope.

    Args:
        success: True when execution completed without replay divergence.
        reason: Optional diagnostic reason for divergence/failure.
        output_payload: Optional output payload from execution.

    """

    success: bool
    reason: str = ""
    output_payload: dict[str, Any] | None = None


class ShadowExecutionCore:
    """Execute replay envelopes under strict side-effect controls."""

    def __init__(
        self,
        *,
        memory_tx_factory: Callable[[], Any],
        storage_tx_factory: Callable[[], Any],
        process_tx_factory: Callable[[], Any],
        context_tx_factory: Callable[[], Any],
        block_network: bool = True,
    ) -> None:
        """Initialize shadow execution dependencies.

        Args:
            memory_tx_factory: Factory for memory transaction wrappers.
            storage_tx_factory: Factory for storage transaction wrappers.
            process_tx_factory: Factory for process transaction wrappers.
            context_tx_factory: Factory for context transaction wrappers.
            block_network: Whether network side-effect intents are blocked.

        """
        self._memory_tx_factory = memory_tx_factory
        self._storage_tx_factory = storage_tx_factory
        self._process_tx_factory = process_tx_factory
        self._context_tx_factory = context_tx_factory
        self._block_network = block_network

    def validate(self) -> None:
        """Validate core dependency configuration.

        Raises:
            ReplayConfigurationError: If a required factory is not callable.

        """
        for name, factory in (
            ("memory_tx_factory", self._memory_tx_factory),
            ("storage_tx_factory", self._storage_tx_factory),
            ("process_tx_factory", self._process_tx_factory),
            ("context_tx_factory", self._context_tx_factory),
        ):
            if not callable(factory):
                raise ReplayConfigurationError(f"Invalid shadow core dependency: {name}")

    async def execute_envelope(
        self,
        envelope: ReplayEnvelope,
        *,
        deterministic_seed: int | None = None,
    ) -> ReplayStepResult:
        """Execute one envelope in side-effect-free mode.

        Args:
            envelope: Envelope to execute.
            deterministic_seed: Optional deterministic seed value for callers.

        Returns:
            Structured replay step result.

        Raises:
            ShadowPolicyViolation: If envelope requests blocked side effects.

        """
        self.validate()
        _ = deterministic_seed

        transactions = [
            self._memory_tx_factory(),
            self._storage_tx_factory(),
            self._process_tx_factory(),
            self._context_tx_factory(),
        ]

        self._assert_shadow_policy(envelope)

        try:
            output_payload = await self._execute_tool_intent(envelope)
            return ReplayStepResult(success=True, output_payload=output_payload)
        except ShadowPolicyViolation:
            await self._rollback_all(transactions)
            raise
        except Exception as exc:  # noqa: BLE001
            await self._rollback_all(transactions)
            return ReplayStepResult(success=False, reason=str(exc), output_payload=None)

    async def _execute_tool_intent(self, envelope: ReplayEnvelope) -> dict[str, Any]:
        """Execute replay tool intent for one envelope.

        Args:
            envelope: Envelope to execute.

        Returns:
            Deterministic output payload.

        """
        return dict(envelope.output_payload)

    def _assert_shadow_policy(self, envelope: ReplayEnvelope) -> None:
        """Validate side-effect intents against shadow policy.

        Args:
            envelope: Envelope containing side-effect intents.

        Raises:
            ShadowPolicyViolation: If any blocked intent is present.

        """
        blocked = {"process", "spawn", "write", "delete", "filesystem", "storage", "network"}
        for intent in envelope.side_effect_intents:
            kind = str(intent.get("kind", "")).strip().lower()
            action = str(intent.get("action", "")).strip().lower()

            if kind in blocked or action in blocked:
                if kind == "network" and not self._block_network:
                    continue
                raise ShadowPolicyViolation(f"Blocked shadow side effect intent: kind={kind}, action={action}")

    async def _rollback_all(self, transactions: list[Any]) -> None:
        """Rollback all active transactions best-effort.

        Args:
            transactions: Transaction instances that may support rollback().

        """
        for transaction in transactions:
            rollback = getattr(transaction, "rollback", None)
            if rollback is not None:
                await rollback()
