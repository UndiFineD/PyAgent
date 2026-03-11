r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/ComplianceAgent.description.md

# ComplianceAgent

**File**: `src\classes\specialized\ComplianceAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 123  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for ComplianceAgent.

## Classes (1)

### `ComplianceAgent`

**Inherits from**: BaseAgent

Phase 57: Data Privacy & Compliance.
Scans memory shards for PII and sensitive data patterns.

**Methods** (7):
- `__init__(self, path)`
- `_record(self, action, findings)`
- `scan_shard(self, shard_data)`
- `mask_pii(self, shard_data)`
- `audit_zk_fusion(self, fusion_input)`
- `generate_privacy_impact_assessment(self, project_data)`
- `_get_pia_recommendations(self, risks)`

## Dependencies

**Imports** (11):
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `src.classes.backend.LocalContextRecorder.LocalContextRecorder`
- `src.classes.base_agent.BaseAgent`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/ComplianceAgent.improvements.md

# Improvements for ComplianceAgent

**File**: `src\classes\specialized\ComplianceAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 123 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ComplianceAgent_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import logging
import re
import time
from pathlib import Path
from typing import Any, Dict, List

from src.classes.backend.LocalContextRecorder import LocalContextRecorder
from src.classes.base_agent import BaseAgent


class ComplianceAgent(BaseAgent):
    """Phase 57: Data Privacy & Compliance.
    Scans memory shards for PII and sensitive data patterns.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.pii_patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b\d{4}-\d{4}-\d{4}-\d{4}\b",
            "phone": r"\b\d{3}-\d{3}-\d{4}\b",
        }

        # Phase 108: Intelligence Recording
        work_root = getattr(self, "_workspace_root", None)
        self.recorder = LocalContextRecorder(Path(work_root)) if work_root else None

    def _record(self, action: str, findings: Any) -> None:
        """Records compliance events for the collective intelligence pool."""
        if self.recorder:
            try:
                meta = {"phase": 108, "type": "compliance", "timestamp": time.time()}
                self.recorder.record_interaction(
                    "compliance", "pii_scan", action, str(findings), meta=meta
                )
            except Exception as e:
                logging.debug(f"ComplianceAgent: Recording failed: {e}")

    def scan_shard(self, shard_data: str) -> Dict[str, Any]:
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

    def mask_pii(self, shard_data: str) -> str:
        """Masks detected PII patterns in the data."""
        masked_data = shard_data
        for label, pattern in self.pii_patterns.items():
            masked_data = re.sub(pattern, f"[MASKED_{label.upper()}]", masked_data)
        return masked_data

    def audit_zk_fusion(self, fusion_input: List[str]) -> bool:
        """Audits Zero-Knowledge fusion inputs for compliance before processing."""
        for item in fusion_input:
            if self.scan_shard(item)["pii_detected"]:
                return False
        return True

    def generate_privacy_impact_assessment(
        self, project_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Phase 240: Conducts a Privacy Impact Assessment (PIA).
        Analyzes data types, retention, and collection purposes.
        """
        score = 100
        risks = []

        # Check for high-risk data types
        pii_found = project_data.get("pii_types", [])
        if any(t in ["ssn", "credit_card", "health_record"] for t in pii_found):
            score -= 40
            risks.append("High-risk PII collection (SSN/Financial/Health)")
        elif len(pii_found) > 0:
            score -= 15
            risks.append(f"Basic PII collection: {', '.join(pii_found)}")

        # Check for data retention policy
        retention = project_data.get("retention_period_days")
        if not retention:
            score -= 20
            risks.append("No clear data retention policy defined")
        elif retention > 365:
            score -= 10
            risks.append(
                f"Long retention period ({retention} days) increases exposure risk"
            )

        # Check for encryption status
        if not project_data.get("encrypted_at_rest", False):
            score -= 25
            risks.append("Data not encrypted at rest")

        # Check for purpose limitation
        if not project_data.get("collection_purpose"):
            score -= 10
            risks.append("Missing explicit collection purpose statement")

        return {
            "pia_score": max(0, score),
            "risk_assessment": (
                "High" if score < 50 else "Medium" if score < 80 else "Low"
            ),
            "findings": risks,
            "recommendations": self._get_pia_recommendations(risks),
            "timestamp": time.time(),
        }

    def _get_pia_recommendations(self, risks: List[str]) -> List[str]:
        recommendations = []
        for risk in risks:
            if "encryption" in risk.lower():
                recommendations.append(
                    "Implement AES-256 encryption at rest for all database shards."
                )
            if "retention" in risk.lower():
                recommendations.append(
                    "Implement automated data pruning for records older than 90 days."
                )
            if "High-risk PII" in risk:
                recommendations.append(
                    "Consider data tokenization or removal of SSN/Financial data if not strictly necessary."
                )
        return recommendations
