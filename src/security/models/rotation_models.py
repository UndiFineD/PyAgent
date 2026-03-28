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

"""Rotation checkpoint and gate decision models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RotationCheckpoint:
    """Tracks rotation evidence state for one incident.

    Attributes:
        incident_id: Incident identifier.
        compromised_fingerprint: Fingerprint of leaked secret.
        required_systems: Systems that must be rotated.
        evidence_by_system: Mapping of system name to evidence URI.

    """

    incident_id: str
    compromised_fingerprint: str
    required_systems: list[str]
    evidence_by_system: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RotationGateDecision:
    """Gate decision returned by rotation checkpoint evaluation.

    Attributes:
        incident_id: Incident identifier.
        status: Gate status: BLOCKED, PARTIAL, or COMPLETE.
        missing_systems: Required systems missing evidence.
        evidence_count: Number of persisted evidence entries.

    """

    incident_id: str
    status: str
    missing_systems: list[str]
    evidence_count: int
