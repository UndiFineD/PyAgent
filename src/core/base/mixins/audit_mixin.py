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

"""Canonical audit mixin implementation for base mixin architecture."""

from __future__ import annotations

from typing import Any

from src.core.base.mixins.base_behavior_mixin import BaseBehaviorMixin


class AuditMixin(BaseBehaviorMixin):
    """Provide optional convenience wrappers around audit-trail core APIs."""

    def _get_audit_trail_core(self) -> Any:
        """Return the configured audit-trail core for this host.

        Returns:
            Configured audit-trail core instance or None when disabled.

        """
        return None

    def audit_emit_event(
        self,
        *,
        event_type: str,
        action: str,
        payload: dict[str, object],
        actor_id: str | None = None,
        target: str | None = None,
        tx_id: str | None = None,
        context_id: str | None = None,
        correlation_id: str | None = None,
    ) -> str | None:
        """Emit an audit event when an audit core is configured.

        Args:
            event_type: Domain event category.
            action: Action performed.
            payload: JSON-like payload dictionary.
            actor_id: Optional actor identifier.
            target: Optional target identifier.
            tx_id: Optional transaction identifier.
            context_id: Optional context identifier.
            correlation_id: Optional correlation identifier.

        Returns:
            Event hash on success, or None when no core is configured.

        """
        self._emit_migration_event("host_contract_validated", {"mixin": "AuditMixin"})

        core: Any = self._get_audit_trail_core()
        append_event_dict = getattr(core, "append_event_dict", None)
        if core is None or not callable(append_event_dict):
            return None

        try:
            event_hash: object = append_event_dict(
                event_type=event_type,
                action=action,
                payload=payload,
                actor_id=actor_id,
                target=target,
                tx_id=tx_id,
                context_id=context_id,
                correlation_id=correlation_id,
            )
            if isinstance(event_hash, str):
                return event_hash
            return None
        except Exception:
            return None

    def audit_emit_success(self, action: str, payload: dict[str, object]) -> str | None:
        """Emit a success-classified audit event.

        Args:
            action: Success action label.
            payload: Event payload.

        Returns:
            Event hash on success, else None.

        """
        return self.audit_emit_event(event_type="audit.success", action=action, payload=payload)

    def audit_emit_failure(self, action: str, payload: dict[str, object]) -> str | None:
        """Emit a failure-classified audit event.

        Args:
            action: Failure action label.
            payload: Event payload.

        Returns:
            Event hash on success, else None.

        """
        return self.audit_emit_event(event_type="audit.failure", action=action, payload=payload)


def validate() -> bool:
    """Validate module contracts are loadable.

    Returns:
        True when this module can be imported.

    """
    return True


__all__ = ["AuditMixin", "validate"]
