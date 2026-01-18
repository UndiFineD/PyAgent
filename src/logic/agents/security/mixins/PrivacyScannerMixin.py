# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.logic.agents.security.ComplianceAgent import ComplianceAgent

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
            "pii_detected": len(findings) > 0,
            "findings": findings,
            "compliant": len(findings) == 0,
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
