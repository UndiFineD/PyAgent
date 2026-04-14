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

"""Rotation checkpoint lifecycle service for remediation incidents."""

from __future__ import annotations

from .models.rotation_models import RotationCheckpoint, RotationGateDecision


class RotationCheckpointService:
    """Manage incident-scoped credential rotation evidence checkpoints."""

    def __init__(self) -> None:
        """Initialize in-memory checkpoint registry."""
        self._incidents: dict[str, RotationCheckpoint] = {}

    def begin_incident(
        self,
        incident_id: str,
        compromised_fingerprint: str,
        required_systems: list[str],
    ) -> RotationCheckpoint:
        """Create and persist a new rotation checkpoint incident.

        Args:
            incident_id: Incident identifier.
            compromised_fingerprint: Fingerprint of leaked material.
            required_systems: Systems that must be rotated.

        Returns:
            Persisted checkpoint object.

        """
        checkpoint = RotationCheckpoint(
            incident_id=incident_id,
            compromised_fingerprint=compromised_fingerprint,
            required_systems=list(required_systems),
        )
        self._incidents[incident_id] = checkpoint
        return checkpoint

    def record_rotation_step(self, incident_id: str, system: str, evidence_uri: str) -> None:
        """Record evidence for one rotated system.

        Args:
            incident_id: Incident identifier.
            system: System name that was rotated.
            evidence_uri: URI that points to rotation evidence.

        Raises:
            ValueError: If incident is unknown or evidence URI is empty.

        """
        if not evidence_uri.strip():
            msg = "evidence_uri is required"
            raise ValueError(msg)
        checkpoint = self._incidents.get(incident_id)
        if checkpoint is None:
            msg = f"incident '{incident_id}' not found"
            raise ValueError(msg)
        checkpoint.evidence_by_system[system] = evidence_uri

    def evaluate_gate(self, incident_id: str) -> RotationGateDecision:
        """Evaluate gate status based on required systems and evidence.

        Args:
            incident_id: Incident identifier.

        Returns:
            Gate decision containing status and missing systems.

        Raises:
            ValueError: If incident is unknown.

        """
        checkpoint = self._incidents.get(incident_id)
        if checkpoint is None:
            msg = f"incident '{incident_id}' not found"
            raise ValueError(msg)

        missing_systems = [
            system for system in checkpoint.required_systems if system not in checkpoint.evidence_by_system
        ]

        if len(missing_systems) == len(checkpoint.required_systems):
            status = "BLOCKED"
        elif missing_systems:
            status = "PARTIAL"
        else:
            status = "COMPLETE"

        return RotationGateDecision(
            incident_id=incident_id,
            status=status,
            missing_systems=missing_systems,
            evidence_count=len(checkpoint.evidence_by_system),
        )
