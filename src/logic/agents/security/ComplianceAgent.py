import re
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
from src.core.base.version import VERSION

__version__ = VERSION

class ComplianceAgent(BaseAgent):
    """
    Phase 57: Data Privacy & Compliance.
    Scans memory shards for PII and sensitive data patterns.
    """
    
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.pii_patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b\d{4}-\d{4}-\d{4}-\d{4}\b",
            "phone": r"\b\d{3}-\d{3}-\d{4}\b"
        }
        
        # Phase 108: Intelligence Recording
        work_root = getattr(self, "_workspace_root", None)
        self.recorder = LocalContextRecorder(Path(work_root)) if work_root else None

    def _record(self, action: str, findings: Any) -> None:
        """Records compliance events for the collective intelligence pool."""
        if self.recorder:
            try:
                meta = {"phase": 108, "type": "compliance", "timestamp": time.time()}
                self.recorder.record_interaction("compliance", "pii_scan", action, str(findings), meta=meta)
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
            "compliant": len(findings) == 0
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
