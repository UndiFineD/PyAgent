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

"""
Privacy scanner mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.logic.agents.security.compliance_agent import ComplianceAgent


class PrivacyScannerMixin:
    """Mixin for PII scanning and masking in ComplianceAgent."""

    def scan_shard(self: ComplianceAgent, shard_data: str) -> dict[str, Any]:
        """Scans a data string for PII patterns."""
        findings = []
        for label, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, shard_data)
            if matches:
                findings.append({"type": label, "count": len(matches)})

        res = {
            "pii_detected": bool(findings),
            "findings": findings,
            "compliant": not findings,
        }

        if res["pii_detected"]:
            self._record("pii_detected", findings)

        return res

    def mask_pii(self: ComplianceAgent, shard_data: str) -> str:
        """Masks detected PII patterns in the data."""
        masked_data = shard_data
        for label, pattern in self.pii_patterns.items():
            masked_data = re.sub(pattern, f"[MASKED_{label.upper()}]", masked_data)
        return masked_data

    def audit_zk_fusion(self: ComplianceAgent, fusion_input: list[str]) -> bool:
        """Audits Zero-Knowledge fusion inputs for compliance before processing."""
        for item in fusion_input:
            if self.scan_shard(item)["pii_detected"]:
                return False
        return True
