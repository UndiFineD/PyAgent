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


from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import logging
import re
from typing import Any, TYPE_CHECKING

__version__ = VERSION

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class ImmunizationOrchestrator:
    """
    Implements Swarm Immunization (Phase 32).
    Collectively identifies and "immunizes" the fleet against adversarial prompt patterns.
    """

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self.threat_signatures: list[str] = []  # List of regex patterns
        self.immunization_log: list[dict[str, Any]] = []

    def scan_for_threats(self, prompt: str) -> bool:
        """
        Scans a prompt against known adversarial signatures.
        """
        for signature in self.threat_signatures:
            if re.search(signature, prompt, re.IGNORECASE):
                logging.warning(
                    f"ImmunizationOrchestrator: Adversarial pattern detected: {signature}"
                )
                return True
        return False

    def immunize(self, adversarial_example: str, label: str) -> str:
        """
        Develops a new signature from an adversarial example.
        """
        logging.info(
            f"ImmunizationOrchestrator: Immunizing fleet against new threat: {label}"
        )

        # In a real system, we'd use an LLM or clustering to generate a clean regex
        # For simulation, we take a substring or simplified pattern
        pattern = re.escape(adversarial_example[:20]) + ".*"

        if pattern not in self.threat_signatures:
            self.threat_signatures.append(pattern)
            self.immunization_log.append(
                {
                    "label": label,
                    "pattern": pattern,
                    "timestamp": logging.time.time() if hasattr(logging, "time") else 0,
                }
            )

            # Broadcast the new antibody to the fleet
            if hasattr(self.fleet, "signals"):
                self.fleet.signals.emit(
                    "FLEET_IMMUNIZED", {"threat": label, "pattern": pattern}
                )

        return pattern

    def get_audit_trail(self) -> list[dict[str, Any]]:
        return self.immunization_log
